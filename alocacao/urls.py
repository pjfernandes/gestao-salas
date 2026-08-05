from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.grade, name='grade'),
    path('imprimir/', views.imprimir, name='imprimir'),
    path('baixar-doc/', views.baixar_doc, name='baixar_doc'),

    # Login / logout
    path('login/', auth_views.LoginView.as_view(
        template_name='alocacao/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # APIs do drag-and-drop
    path('api/mover/', views.api_mover, name='api_mover'),
    path('api/remover/<int:pk>/', views.api_remover, name='api_remover'),
    path('api/sugerir/', views.api_sugerir, name='api_sugerir'),
    path('api/turma/<int:pk>/', views.api_turma_detalhe, name='api_turma_detalhe'),

    # CRUD simples
    path('turma/nova/', views.turma_criar, name='turma_criar'),
    path('turma/<int:pk>/editar/', views.turma_editar, name='turma_editar'),
    path('turma/<int:pk>/deletar/', views.turma_deletar, name='turma_deletar'),
    path('sala/nova/', views.sala_criar, name='sala_criar'),
]
