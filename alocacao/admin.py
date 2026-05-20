from django.contrib import admin
from .models import Sala, Turma, Alocacao


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'bloco', 'capacidade', 'eh_laboratorio', 'observacao')
    list_filter = ('bloco', 'eh_laboratorio')
    search_fields = ('numero',)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('codigo_disciplina', 'nome_disciplina', 'codigo_turma',
                    'professor', 'num_alunos', 'exige_laboratorio', 'departamento')
    list_filter = ('departamento', 'exige_laboratorio')
    search_fields = ('nome_disciplina', 'professor', 'codigo_disciplina')


@admin.register(Alocacao)
class AlocacaoAdmin(admin.ModelAdmin):
    list_display = ('turma', 'sala', 'dia_semana', 'hora_inicio', 'hora_fim')
    list_filter = ('dia_semana', 'sala__bloco')
