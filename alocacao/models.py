"""
Modelo enxuto: Sala, Turma e Alocacao.

A Turma carrega a disciplina (código, nome, professor) "embutida" para evitar
cadastros separados. Marco quer rapidez, não burocracia.

A Alocacao é a ligação turma <-> sala em um dia/horário específico.
Uma turma pode ter várias alocações (vários encontros na semana).
"""
from django.db import models


DIAS_SEMANA = [
    (1, 'Segunda-feira'),
    (2, 'Terça-feira'),
    (3, 'Quarta-feira'),
    (4, 'Quinta-feira'),
    (5, 'Sexta-feira'),
]

# Faixas de horário usadas pelo Instituto (espelho do quadro em papel).
FAIXAS_HORARIO = [
    ('07:00', '09:00'),
    ('09:00', '11:00'),
    ('11:00', '13:00'),
    ('14:00', '16:00'),
    ('16:00', '18:00'),
    ('18:00', '20:00'),
    ('20:00', '22:00'),
]


class Sala(models.Model):
    BLOCOS = [('O', 'Bloco O'), ('P', 'Bloco P')]
    numero = models.CharField(max_length=10)
    bloco = models.CharField(max_length=1, choices=BLOCOS)
    capacidade = models.PositiveIntegerField()
    eh_laboratorio = models.BooleanField(default=False)
    observacao = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['bloco', 'numero']
        unique_together = [('numero', 'bloco')]

    def __str__(self):
        lab = ' (Lab)' if self.eh_laboratorio else ''
        return f'{self.numero}-{self.bloco}{lab} • {self.capacidade}'


class Turma(models.Model):
    DEPARTAMENTOS = [
        ('GGE', 'Geografia'),
        ('GAG', 'Análise Geoambiental'),
        ('GGO', 'Geologia e Geofísica'),
        ('PPGEO', 'PG Geografia'),
        ('PPGDOT', 'PG Din. Oceanos e Terra'),
        ('EXT', 'Outros / Externo'),
    ]
    codigo_disciplina = models.CharField(max_length=20)
    nome_disciplina = models.CharField(max_length=200)
    codigo_turma = models.CharField(max_length=10, default='A1')
    professor = models.CharField(max_length=120, blank=True)
    num_alunos = models.PositiveIntegerField(default=30)
    exige_laboratorio = models.BooleanField(default=False)
    departamento = models.CharField(max_length=10, choices=DEPARTAMENTOS, default='GGE')
    observacao = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['departamento', 'nome_disciplina', 'codigo_turma']

    def __str__(self):
        return f'{self.nome_disciplina} ({self.codigo_turma}) — {self.professor}'

    @property
    def cor(self):
        """Cor estável por departamento (Tailwind classes)."""
        mapa = {
            'GGE': 'bg-blue-100 border-blue-400 text-blue-900',
            'GAG': 'bg-emerald-100 border-emerald-400 text-emerald-900',
            'GGO': 'bg-amber-100 border-amber-400 text-amber-900',
            'PPGEO': 'bg-purple-100 border-purple-400 text-purple-900',
            'PPGDOT': 'bg-pink-100 border-pink-400 text-pink-900',
            'EXT': 'bg-slate-100 border-slate-400 text-slate-900',
        }
        return mapa.get(self.departamento, 'bg-slate-100 border-slate-400')


class Alocacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alocacoes')
    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='alocacoes')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.CharField(max_length=5)  # ex: '09:00'
    hora_fim = models.CharField(max_length=5)     # ex: '11:00'

    class Meta:
        ordering = ['dia_semana', 'hora_inicio']
        verbose_name = 'Alocação'
        verbose_name_plural = 'Alocações'

    def __str__(self):
        sala = self.sala.numero + '-' + self.sala.bloco if self.sala else 'sem sala'
        return f'{self.turma} • {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fim} • {sala}'

    def conflito_sala(self):
        """Retorna QuerySet com outras alocações que conflitam na mesma sala/dia/horário."""
        if not self.sala:
            return Alocacao.objects.none()
        return Alocacao.objects.filter(
            sala=self.sala,
            dia_semana=self.dia_semana,
        ).exclude(pk=self.pk).filter(
            # sobreposição de intervalos
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio,
        )
