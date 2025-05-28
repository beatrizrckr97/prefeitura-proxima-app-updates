from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_solicitacoes, name='lista_solicitacoes'),
    path('nova/', views.nova_solicitacao, name='nova_solicitacao'),
]
