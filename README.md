# Gestão de Salas

Sistema web Django para montar, ajustar e imprimir quadros de horários de
salas de aula. Interface visual com **arrastar-e-soltar**, validação
automática de conflitos (capacidade, laboratório, sobreposição de horário) e
exportação para impressão.

Os dados pré-carregados pelo `seed` são **fictícios** (para demonstração).

## Pré-requisitos

- Python 3.10+
- pip
- git

## Como rodar

```bash
# 1. Clone
git clone https://github.com/SEU_USUARIO/gestao-salas.git
cd gestao-salas

# 2. Ambiente virtual
python -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows

# 3. Dependências
pip install -r requirements.txt

# 4. Banco + dados de demonstração
python manage.py migrate
python manage.py seed

# 5. (opcional) usuário admin
python manage.py createsuperuser

# 6. Servidor
python manage.py runserver
```

Acesse **http://127.0.0.1:8000**.

Para recomeçar do zero: `python manage.py seed --limpar`

## Como usar

- **Topo**: escolha bloco e dia da semana.
- **Painel esquerdo**: turmas pendentes e formulários rápidos para
  adicionar turma e sala.
- **Grade central**: arraste cartões para alocar; arraste para fora para
  desalocar. Verde/amarelo = válido, vermelho = inválido.
- **Hover sobre o cartão**: ✎ edita, × apaga (com confirmação).
- **🖨 Imprimir**: layout em planilha por dia (Ctrl+P → PDF ou impressora).
- **/admin**: cadastro tradicional do Django.

## Stack

Django 4.2+, SQLite, Tailwind (CDN), SortableJS, Vanilla JS.

## Estrutura

```
gestao-salas/
├── manage.py
├── requirements.txt
├── gestao_salas/        # config do projeto
└── alocacao/            # app principal
    ├── models.py        # Sala, Turma, Alocacao
    ├── views.py         # páginas + APIs
    ├── templates/alocacao/
    └── management/commands/seed.py
```

## Comandos úteis

| Comando | Descrição |
|---|---|
| `python manage.py runserver` | Sobe servidor de desenvolvimento |
| `python manage.py seed` | Carrega dados fictícios |
| `python manage.py seed --limpar` | Limpa tudo e recarrega |
| `python manage.py dumpdata alocacao --indent 2 > backup.json` | Backup |
| `python manage.py loaddata backup.json` | Restaura backup |

## Licença

MIT.
