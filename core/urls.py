from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importa as views de autenticação do Django

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('solicitacoes.urls')),  # Suas URLs do app solicitacoes
    # URLs para login e logout
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
