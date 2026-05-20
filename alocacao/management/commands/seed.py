"""
Popula o banco com dados fictícios para demonstração.

Códigos de disciplina, nomes de disciplinas e nomes de professores são
completamente inventados. Use este seed para apresentações, vídeos
demonstrativos e repositórios públicos.
"""
from django.core.management.base import BaseCommand
from alocacao.models import Sala, Turma, Alocacao


# ---------------------------------------------------------------------------
# Salas (fictícias mas plausíveis: dois blocos, alguns laboratórios)
# ---------------------------------------------------------------------------
SALAS = [
    # Bloco O
    ('201', 'O', 60, False),
    ('203', 'O', 30, False),
    ('204', 'O', 60, False),
    ('206', 'O', 50, False),
    ('207', 'O', 40, True),   # Lab
    ('208', 'O', 60, False),
    ('213', 'O', 20, True),   # Lab
    ('307', 'O', 72, False),
    # Bloco P
    ('301', 'P', 32, False),
    ('302', 'P', 40, False),
    ('303', 'P', 34, False),
    ('304', 'P', 45, False),
    ('305', 'P', 40, False),
    ('306', 'P', 45, False),
    ('307', 'P', 50, False),
    ('309', 'P', 40, True),   # Lab
]


# ---------------------------------------------------------------------------
# Turmas (códigos, disciplinas e professores fictícios)
# Formato: (codigo, nome, turma, professor, num_alunos, exige_lab, dept, obs)
# ---------------------------------------------------------------------------
TURMAS = [
    # ---- Departamento A ----
    ('DSC001', 'Introdução às Ciências da Terra', 'A1', 'Ana', 60, False, 'GGE', ''),
    ('DSC002', 'Métodos Quantitativos I', 'A1', 'Bruno', 50, False, 'GGE', ''),
    ('DSC003', 'Cartografia Básica', 'A1', 'Carla', 55, False, 'GGE', ''),
    ('DSC004', 'Geomorfologia I', 'A1', 'Diego', 60, False, 'GGE', ''),
    ('DSC005', 'Geomorfologia II', 'A1', 'Diego', 45, False, 'GGE', ''),
    ('DSC006', 'Climatologia Geral', 'A1', 'Eduarda', 60, False, 'GGE', ''),
    ('DSC007', 'Hidrologia Aplicada', 'A1', 'Fernando', 50, False, 'GGE', 'noturno'),
    ('DSC008', 'Estudos Urbanos', 'A1', 'Gabriela', 60, False, 'GGE', ''),
    ('DSC009', 'Estudos Rurais', 'A1', 'Henrique', 50, False, 'GGE', ''),
    ('DSC010', 'Pesquisa em Ciências Sociais', 'A1', 'Isabel', 40, False, 'GGE', 'noturno'),
    ('DSC011', 'Teoria do Conhecimento', 'A1', 'João', 60, False, 'GGE', ''),
    ('DSC012', 'História do Pensamento Científico', 'A1', 'Karen', 60, False, 'GGE', ''),
    ('DSC013', 'Metodologia da Pesquisa', 'A1', 'Karen', 60, False, 'GGE', 'noturno'),
    ('DSC014', 'Estudos Regionais I', 'A1', 'Luis', 55, False, 'GGE', ''),
    ('DSC015', 'Estudos Regionais II', 'A1', 'Luis', 55, False, 'GGE', ''),

    # ---- Departamento B ----
    ('DSC020', 'Educação Ambiental', 'A1', 'Mariana', 45, False, 'GAG', ''),
    ('DSC021', 'Geoprocessamento I', 'A1', 'Nilson', 40, True, 'GAG', 'laboratório'),
    ('DSC022', 'Geoprocessamento II', 'A1', 'Nilson', 40, True, 'GAG', 'laboratório'),
    ('DSC023', 'Sensoriamento Remoto', 'A1', 'Otávio', 40, True, 'GAG', 'laboratório'),
    ('DSC023', 'Sensoriamento Remoto', 'A2', 'Paula', 40, True, 'GAG', 'laboratório'),
    ('DSC024', 'Análise Espacial', 'A1', 'Paula', 35, False, 'GAG', ''),
    ('DSC025', 'Áreas Protegidas', 'A1', 'Renato', 30, False, 'GAG', ''),
    ('DSC026', 'Gestão Ambiental', 'A1', 'Sofia', 40, False, 'GAG', 'noturno'),
    ('DSC027', 'Resíduos Sólidos', 'A1', 'Tomás', 30, False, 'GAG', ''),
    ('DSC028', 'Avaliação de Impactos', 'A1', 'Vanessa', 45, False, 'GAG', ''),
    ('DSC029', 'Topografia I', 'A1', 'Ana', 25, False, 'GAG', ''),
    ('DSC029', 'Topografia I', 'A2', 'Bruno', 25, False, 'GAG', ''),

    # ---- Departamento C ----
    ('DSC040', 'Fundamentos de Geologia', 'A1', 'Carla', 60, False, 'GGO', ''),
    ('DSC041', 'Mineralogia', 'A1', 'Diego', 45, False, 'GGO', ''),
    ('DSC042', 'Petrologia', 'A1', 'Eduarda', 40, False, 'GGO', ''),
    ('DSC043', 'Estratigrafia', 'A1', 'Fernando', 40, False, 'GGO', ''),
    ('DSC044', 'Geofísica Aplicada', 'A1', 'Gabriela', 30, True, 'GGO', 'laboratório'),
    ('DSC045', 'Sismologia Básica', 'A1', 'Henrique', 25, True, 'GGO', 'laboratório, noturno'),
    ('DSC046', 'Oceanografia Geral', 'A1', 'Isabel', 45, False, 'GGO', ''),
    ('DSC047', 'Recursos Minerais', 'A1', 'João', 35, False, 'GGO', 'noturno'),

    # ---- Pós-Graduação I ----
    ('PG001', 'Seminários Avançados', 'A1', 'Karen', 25, False, 'PPGEO', 'sala fixa 305-P'),
    ('PG002', 'Tópicos Especiais I', 'A1', 'Luis', 20, False, 'PPGEO', 'noturno'),

    # ---- Pós-Graduação II ----
    ('PG010', 'Programação Científica', 'A1', 'Mariana', 25, True, 'PPGDOT', 'laboratório'),
    ('PG011', 'Análise de Dados Aplicada', 'A1', 'Nilson', 20, True, 'PPGDOT', 'laboratório, noturno'),

    # ---- Externo / outros cursos ----
    ('EXT001', 'Disciplina Compartilhada I', 'A1', 'Otávio', 50, False, 'EXT', ''),
    ('EXT002', 'Disciplina Compartilhada II', 'A1', 'Paula', 55, False, 'EXT', 'noturno'),
]


# ---------------------------------------------------------------------------
# Alocações fictícias — formam uma grade visualmente rica para demo
# Formato: (cod_disciplina, cod_turma, sala_num, sala_bloco, dia, hi, hf)
# Dias: 1=segunda, 2=terça, 3=quarta, 4=quinta, 5=sexta
# ---------------------------------------------------------------------------
ALOCACOES = [
    # ============= SEGUNDA =============
    # Bloco O
    ('DSC001', 'A1', '307', 'O', 1, '09:00', '11:00'),
    ('DSC001', 'A1', '307', 'O', 1, '11:00', '13:00'),
    ('DSC003', 'A1', '208', 'O', 1, '09:00', '11:00'),
    ('DSC003', 'A1', '208', 'O', 1, '11:00', '13:00'),
    ('DSC021', 'A1', '207', 'O', 1, '14:00', '16:00'),
    ('DSC021', 'A1', '207', 'O', 1, '16:00', '18:00'),
    ('DSC011', 'A1', '307', 'O', 1, '18:00', '20:00'),
    ('DSC011', 'A1', '307', 'O', 1, '20:00', '22:00'),
    ('DSC026', 'A1', '204', 'O', 1, '18:00', '20:00'),
    ('DSC026', 'A1', '204', 'O', 1, '20:00', '22:00'),
    # Bloco P
    ('PG001', 'A1', '305', 'P', 1, '09:00', '11:00'),
    ('PG001', 'A1', '305', 'P', 1, '11:00', '13:00'),
    ('DSC040', 'A1', '307', 'P', 1, '09:00', '11:00'),
    ('DSC040', 'A1', '307', 'P', 1, '11:00', '13:00'),
    ('DSC044', 'A1', '309', 'P', 1, '14:00', '16:00'),
    ('DSC044', 'A1', '309', 'P', 1, '16:00', '18:00'),
    ('DSC047', 'A1', '303', 'P', 1, '18:00', '20:00'),
    ('DSC047', 'A1', '303', 'P', 1, '20:00', '22:00'),

    # ============= TERÇA =============
    # Bloco O
    ('DSC012', 'A1', '307', 'O', 2, '09:00', '11:00'),
    ('DSC012', 'A1', '307', 'O', 2, '11:00', '13:00'),
    ('DSC002', 'A1', '208', 'O', 2, '09:00', '11:00'),
    ('DSC002', 'A1', '208', 'O', 2, '11:00', '13:00'),
    ('DSC023', 'A1', '207', 'O', 2, '14:00', '16:00'),
    ('DSC023', 'A1', '207', 'O', 2, '16:00', '18:00'),
    ('DSC020', 'A1', '206', 'O', 2, '14:00', '16:00'),
    ('DSC020', 'A1', '206', 'O', 2, '16:00', '18:00'),
    ('DSC007', 'A1', '307', 'O', 2, '18:00', '20:00'),
    ('DSC007', 'A1', '307', 'O', 2, '20:00', '22:00'),
    ('DSC045', 'A1', '213', 'O', 2, '18:00', '20:00'),
    ('DSC045', 'A1', '213', 'O', 2, '20:00', '22:00'),
    # Bloco P
    ('DSC041', 'A1', '306', 'P', 2, '09:00', '11:00'),
    ('DSC041', 'A1', '306', 'P', 2, '11:00', '13:00'),
    ('DSC029', 'A1', '301', 'P', 2, '09:00', '11:00'),
    ('DSC029', 'A1', '301', 'P', 2, '11:00', '13:00'),
    ('DSC024', 'A1', '303', 'P', 2, '14:00', '16:00'),
    ('DSC024', 'A1', '303', 'P', 2, '16:00', '18:00'),

    # ============= QUARTA =============
    # Bloco O
    ('DSC004', 'A1', '307', 'O', 3, '09:00', '11:00'),
    ('DSC004', 'A1', '307', 'O', 3, '11:00', '13:00'),
    ('DSC008', 'A1', '208', 'O', 3, '09:00', '11:00'),
    ('DSC008', 'A1', '208', 'O', 3, '11:00', '13:00'),
    ('DSC022', 'A1', '207', 'O', 3, '09:00', '11:00'),
    ('DSC022', 'A1', '207', 'O', 3, '11:00', '13:00'),
    ('DSC027', 'A1', '203', 'O', 3, '14:00', '16:00'),
    ('DSC027', 'A1', '203', 'O', 3, '16:00', '18:00'),
    ('DSC028', 'A1', '206', 'O', 3, '14:00', '16:00'),
    ('DSC028', 'A1', '206', 'O', 3, '16:00', '18:00'),
    ('DSC013', 'A1', '307', 'O', 3, '18:00', '20:00'),
    ('DSC013', 'A1', '307', 'O', 3, '20:00', '22:00'),
    # Bloco P
    ('PG010', 'A1', '309', 'P', 3, '09:00', '11:00'),
    ('PG010', 'A1', '309', 'P', 3, '11:00', '13:00'),
    ('DSC042', 'A1', '306', 'P', 3, '09:00', '11:00'),
    ('DSC042', 'A1', '306', 'P', 3, '11:00', '13:00'),
    ('PG011', 'A1', '309', 'P', 3, '18:00', '20:00'),
    ('PG011', 'A1', '309', 'P', 3, '20:00', '22:00'),

    # ============= QUINTA =============
    # Bloco O
    ('DSC012', 'A1', '307', 'O', 4, '09:00', '11:00'),
    ('DSC012', 'A1', '307', 'O', 4, '11:00', '13:00'),
    ('DSC002', 'A1', '208', 'O', 4, '09:00', '11:00'),
    ('DSC002', 'A1', '208', 'O', 4, '11:00', '13:00'),
    ('DSC023', 'A2', '207', 'O', 4, '14:00', '16:00'),
    ('DSC023', 'A2', '207', 'O', 4, '16:00', '18:00'),
    ('DSC010', 'A1', '204', 'O', 4, '18:00', '20:00'),
    ('DSC010', 'A1', '204', 'O', 4, '20:00', '22:00'),
    ('DSC006', 'A1', '307', 'O', 4, '18:00', '20:00'),
    ('DSC006', 'A1', '307', 'O', 4, '20:00', '22:00'),
    # Bloco P
    ('DSC029', 'A2', '301', 'P', 4, '09:00', '11:00'),
    ('DSC029', 'A2', '301', 'P', 4, '11:00', '13:00'),
    ('DSC043', 'A1', '306', 'P', 4, '09:00', '11:00'),
    ('DSC043', 'A1', '306', 'P', 4, '11:00', '13:00'),
    ('DSC046', 'A1', '307', 'P', 4, '09:00', '11:00'),
    ('DSC046', 'A1', '307', 'P', 4, '11:00', '13:00'),

    # ============= SEXTA =============
    # Bloco O
    ('DSC014', 'A1', '208', 'O', 5, '09:00', '11:00'),
    ('DSC014', 'A1', '208', 'O', 5, '11:00', '13:00'),
    ('DSC015', 'A1', '307', 'O', 5, '09:00', '11:00'),
    ('DSC015', 'A1', '307', 'O', 5, '11:00', '13:00'),
    ('EXT001', 'A1', '307', 'O', 5, '14:00', '16:00'),
    ('EXT001', 'A1', '307', 'O', 5, '16:00', '18:00'),
    ('EXT002', 'A1', '208', 'O', 5, '18:00', '20:00'),
    ('EXT002', 'A1', '208', 'O', 5, '20:00', '22:00'),
    # Bloco P
    ('PG002', 'A1', '305', 'P', 5, '18:00', '20:00'),
    ('PG002', 'A1', '305', 'P', 5, '20:00', '22:00'),
    ('DSC025', 'A1', '303', 'P', 5, '14:00', '16:00'),
    ('DSC025', 'A1', '303', 'P', 5, '16:00', '18:00'),
]


class Command(BaseCommand):
    help = 'Carrega salas e turmas iniciais (dados fictícios para demonstração).'

    def add_arguments(self, parser):
        parser.add_argument('--limpar', action='store_true',
                            help='Apaga dados existentes antes de popular.')

    def handle(self, *args, **opts):
        if opts['limpar']:
            Alocacao.objects.all().delete()
            Turma.objects.all().delete()
            Sala.objects.all().delete()
            self.stdout.write(self.style.WARNING('Base limpa.'))

        # Salas
        for num, bloco, cap, lab in SALAS:
            Sala.objects.update_or_create(
                numero=num, bloco=bloco,
                defaults={'capacidade': cap, 'eh_laboratorio': lab},
            )
        self.stdout.write(self.style.SUCCESS(f'{Sala.objects.count()} salas.'))

        # Turmas
        for cod, nome, tu, prof, alunos, lab, dept, obs in TURMAS:
            Turma.objects.update_or_create(
                codigo_disciplina=cod, codigo_turma=tu,
                defaults={
                    'nome_disciplina': nome, 'professor': prof,
                    'num_alunos': alunos, 'exige_laboratorio': lab,
                    'departamento': dept, 'observacao': obs,
                },
            )
        self.stdout.write(self.style.SUCCESS(f'{Turma.objects.count()} turmas.'))

        # Alocações
        criadas, faltando = 0, []
        for cod, tu, sala_num, sala_bloco, dia, hi, hf in ALOCACOES:
            try:
                turma = Turma.objects.get(codigo_disciplina=cod, codigo_turma=tu)
                sala = Sala.objects.get(numero=sala_num, bloco=sala_bloco)
            except (Turma.DoesNotExist, Sala.DoesNotExist):
                faltando.append((cod, tu))
                continue
            Alocacao.objects.get_or_create(
                turma=turma, sala=sala, dia_semana=dia,
                hora_inicio=hi, hora_fim=hf,
            )
            criadas += 1
        self.stdout.write(self.style.SUCCESS(f'{criadas} alocações.'))
        if faltando:
            self.stdout.write(self.style.WARNING(
                f'{len(faltando)} alocações ignoradas (turma/sala não encontrada).'))
