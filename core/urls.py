
from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.home, name='home'),
    path('novo-chamado/', views.novo_chamado, name='novo_chamado'),
    path('ver-chamado/<int:chamado_id>/', views.ver_chamado, name='ver_chamado'),
    path('editar-chamado/<int:chamado_id>/', views.editar_chamado, name='editar_chamado'),
    path('excluir-chamado/<int:chamado_id>/', views.excluir_chamado, name='excluir_chamado'),
]
