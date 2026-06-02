"""Views: grade interativa + APIs simples para drag-and-drop + impressão."""
import json
from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Sala, Turma, Alocacao, DIAS_SEMANA, FAIXAS_HORARIO


def api_login_required(view):
    """Como @login_required, mas devolve JSON 403 em vez de redirecionar.

    Usado nos endpoints de API (chamados via fetch/AJAX), onde um redirect
    para a tela de login quebraria o JavaScript.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'ok': False, 'erro': 'Faça login para editar o quadro.'},
                status=403,
            )
        return view(request, *args, **kwargs)
    return wrapper

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _intervalos_se_sobrepoem(a_ini, a_fim, b_ini, b_fim):
    """Strings 'HH:MM' — verdadeiro se houver sobreposição."""
    return a_ini < b_fim and b_ini < a_fim


def _validar_alocacao(turma, sala, dia, hora_inicio, hora_fim, ignorar_id=None):
    """Aplica as regras de negócio. Retorna (ok, mensagem)."""
    if sala is None:
        return True, ''

    if sala.capacidade < turma.num_alunos:
        return False, (
            f'A sala {sala.numero}-{sala.bloco} comporta {sala.capacidade} alunos, '
            f'mas a turma tem {turma.num_alunos}.'
        )

    conflitantes = Alocacao.objects.filter(sala=sala, dia_semana=dia)
    if ignorar_id:
        conflitantes = conflitantes.exclude(pk=ignorar_id)
    for outra in conflitantes:
        if _intervalos_se_sobrepoem(hora_inicio, hora_fim, outra.hora_inicio, outra.hora_fim):
            return False, (
                f'Sala já ocupada por "{outra.turma.nome_disciplina}" '
                f'({outra.turma.codigo_turma}) das {outra.hora_inicio} às {outra.hora_fim}.'
            )

    return True, ''

def _sugerir_sala(turma, dia, hora_inicio, hora_fim, bloco=None):
    qs = Sala.objects.all()
    if bloco:
        qs = qs.filter(bloco=bloco)
    if turma.exige_laboratorio:
        qs = qs.filter(eh_laboratorio=True)
    qs = qs.filter(capacidade__gte=turma.num_alunos).order_by('capacidade')

    for sala in qs:
        ok, _ = _validar_alocacao(turma, sala, dia, hora_inicio, hora_fim)
        if ok:
            return sala
    return None


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def grade(request):
    """Tela principal: grade visual interativa."""
    bloco = request.GET.get('bloco', 'O')
    dia = int(request.GET.get('dia', 1))

    salas = list(Sala.objects.filter(bloco=bloco))
    alocacoes = (Alocacao.objects
                 .filter(dia_semana=dia, sala__bloco=bloco)
                 .select_related('turma', 'sala'))

    mapa = {}
    for a in alocacoes:
        mapa.setdefault((a.sala_id, a.hora_inicio), []).append(a)

    linhas = []
    for ini, fim in FAIXAS_HORARIO:
        celulas = []
        for sala in salas:
            celulas.append({
                'sala': sala,
                'alocacoes': mapa.get((sala.id, ini), []),
            })
        linhas.append({'inicio': ini, 'fim': fim, 'celulas': celulas})

    # Painel mostra TODAS as turmas (reutilizáveis), com nº de encontros já alocados.
    from django.db.models import Count
    turmas_painel = (Turma.objects
                     .annotate(n_aloc=Count('alocacoes'))
                     .order_by('departamento', 'nome_disciplina', 'codigo_turma'))

    # Mapa turma -> lista de alocacoes (alimenta o balao "localizar no quadro").
    dias_nome = dict(DIAS_SEMANA)
    aloc_por_turma = {}
    for a in (Alocacao.objects
              .select_related('sala')
              .order_by('dia_semana', 'hora_inicio')):
        aloc_por_turma.setdefault(a.turma_id, []).append({
            'id': a.id,
            'dia': a.dia_semana,
            'dia_nome': dias_nome.get(a.dia_semana, ''),
            'bloco': a.sala.bloco if a.sala else None,
            'sala': (f'{a.sala.numero}-{a.sala.bloco}' if a.sala else 'sem sala'),
            'hora_inicio': a.hora_inicio,
            'hora_fim': a.hora_fim,
        })

    return render(request, 'alocacao/grade.html', {
        'bloco': bloco,
        'dia': dia,
        'dias': DIAS_SEMANA,
        'salas': salas,
        'linhas': linhas,
        'pendentes': turmas_painel,
        'faixas': FAIXAS_HORARIO,
        'departamentos': Turma.DEPARTAMENTOS,
        'pode_editar': request.user.is_authenticated,
        'aloc_por_turma': aloc_por_turma,
    })


@login_required
def imprimir(request):
    bloco = request.GET.get('bloco', 'O')
    salas = list(Sala.objects.filter(bloco=bloco))

    quadros = []
    for dia_num, dia_nome in DIAS_SEMANA:
        alocs = (Alocacao.objects
                 .filter(dia_semana=dia_num, sala__bloco=bloco)
                 .select_related('turma', 'sala'))
        mapa = {}
        for a in alocs:
            mapa.setdefault((a.sala_id, a.hora_inicio), []).append(a)

        linhas = []
        for ini, fim in FAIXAS_HORARIO:
            celulas = []
            for sala in salas:
                celulas.append({
                    'sala': sala,
                    'alocacoes': mapa.get((sala.id, ini), []),
                })
            linhas.append({'inicio': ini, 'fim': fim, 'celulas': celulas})
        quadros.append({'dia': dia_nome, 'linhas': linhas})

    return render(request, 'alocacao/imprimir.html', {
        'bloco': bloco,
        'salas': salas,
        'quadros': quadros,
    })


# ---------------------------------------------------------------------------
# APIs (JSON) — drag-and-drop
# ---------------------------------------------------------------------------

@api_login_required
@require_POST
def api_mover(request):
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON inválido')

    sala = Sala.objects.filter(pk=data.get('sala_id')).first() if data.get('sala_id') else None
    dia = int(data['dia'])
    hi, hf = data['hora_inicio'], data['hora_fim']

    if data.get('alocacao_id'):
        aloc = get_object_or_404(Alocacao, pk=data['alocacao_id'])
        turma = aloc.turma
        ignorar = aloc.id
    else:
        turma = get_object_or_404(Turma, pk=data['turma_id'])
        aloc = None
        ignorar = None

    ok, msg = _validar_alocacao(turma, sala, dia, hi, hf, ignorar_id=ignorar)
    if not ok:
        return JsonResponse({'ok': False, 'erro': msg}, status=400)

    if aloc:
        aloc.sala = sala
        aloc.dia_semana = dia
        aloc.hora_inicio = hi
        aloc.hora_fim = hf
        aloc.save()
    else:
        aloc = Alocacao.objects.create(
            turma=turma, sala=sala, dia_semana=dia,
            hora_inicio=hi, hora_fim=hf,
        )

    return JsonResponse({'ok': True, 'alocacao_id': aloc.id})


@api_login_required
@require_POST
def api_remover(request, pk):
    aloc = get_object_or_404(Alocacao, pk=pk)
    aloc.delete()
    return JsonResponse({'ok': True})


@api_login_required
@require_POST
def api_sugerir(request):
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON inválido')

    turma = get_object_or_404(Turma, pk=data['turma_id'])
    sala = _sugerir_sala(
        turma,
        int(data['dia']),
        data['hora_inicio'],
        data['hora_fim'],
        bloco=data.get('bloco'),
    )
    if not sala:
        return JsonResponse({'ok': False, 'erro': 'Nenhuma sala compatível disponível.'})
    return JsonResponse({
        'ok': True,
        'sala_id': sala.id,
        'sala_label': f'{sala.numero}-{sala.bloco}',
    })


# ---------------------------------------------------------------------------
# Turma — criar, ver, editar, deletar
# ---------------------------------------------------------------------------

@login_required
@require_POST
def turma_criar(request):
    Turma.objects.create(
        codigo_disciplina=request.POST.get('codigo_disciplina', ''),
        nome_disciplina=request.POST.get('nome_disciplina', '').strip() or 'Sem nome',
        codigo_turma=request.POST.get('codigo_turma', 'A1'),
        professor=request.POST.get('professor', ''),
        num_alunos=int(request.POST.get('num_alunos') or 30),
        exige_laboratorio=request.POST.get('exige_laboratorio') == 'on',
        departamento=request.POST.get('departamento', 'GGE'),
        observacao=request.POST.get('observacao', ''),
    )
    return redirect(request.META.get('HTTP_REFERER', 'grade'))


@api_login_required
@require_GET
def api_turma_detalhe(request, pk):
    """Devolve dados de uma turma em JSON — usado pelo modal de edição."""
    t = get_object_or_404(Turma, pk=pk)
    return JsonResponse({
        'id': t.id,
        'codigo_disciplina': t.codigo_disciplina,
        'nome_disciplina': t.nome_disciplina,
        'codigo_turma': t.codigo_turma,
        'professor': t.professor,
        'num_alunos': t.num_alunos,
        'exige_laboratorio': t.exige_laboratorio,
        'departamento': t.departamento,
        'observacao': t.observacao,
    })


@login_required
@require_POST
def turma_editar(request, pk):
    """Edita uma turma via form normal e volta para a grade."""
    t = get_object_or_404(Turma, pk=pk)
    t.codigo_disciplina = request.POST.get('codigo_disciplina', t.codigo_disciplina)
    t.nome_disciplina = request.POST.get('nome_disciplina', '').strip() or t.nome_disciplina
    t.codigo_turma = request.POST.get('codigo_turma', t.codigo_turma)
    t.professor = request.POST.get('professor', t.professor)
    try:
        t.num_alunos = int(request.POST.get('num_alunos') or t.num_alunos)
    except ValueError:
        pass
    t.exige_laboratorio = request.POST.get('exige_laboratorio') == 'on'
    t.departamento = request.POST.get('departamento', t.departamento)
    t.observacao = request.POST.get('observacao', t.observacao)
    t.save()

    # Se a edição deixou alguma alocação inválida (mudou nº de alunos ou exigência
    # de lab), revalida cada alocação dela e desvincula da sala se ficou ruim.
    for a in t.alocacoes.select_related('sala').all():
        if a.sala is None:
            continue
        ok, _ = _validar_alocacao(t, a.sala, a.dia_semana, a.hora_inicio, a.hora_fim,
                                  ignorar_id=a.id)
        if not ok:
            a.sala = None
            a.save()

    return redirect(request.META.get('HTTP_REFERER', 'grade'))


@login_required
@require_POST
def turma_deletar(request, pk):
    """Apaga a turma e, em cascata, todas as suas alocações."""
    t = get_object_or_404(Turma, pk=pk)
    t.delete()
    return redirect(request.META.get('HTTP_REFERER', 'grade'))


# ---------------------------------------------------------------------------
# Sala — criar
# ---------------------------------------------------------------------------

@login_required
@require_POST
def sala_criar(request):
    numero = request.POST.get('numero', '').strip()
    bloco = request.POST.get('bloco', 'O')
    if not numero:
        return redirect(request.META.get('HTTP_REFERER', 'grade'))
    try:
        capacidade = int(request.POST.get('capacidade') or 30)
    except ValueError:
        capacidade = 30
    Sala.objects.update_or_create(
        numero=numero, bloco=bloco,
        defaults={
            'capacidade': capacidade,
            'eh_laboratorio': request.POST.get('eh_laboratorio') == 'on',
            'observacao': request.POST.get('observacao', ''),
        },
    )
    return redirect(request.META.get('HTTP_REFERER', 'grade'))
