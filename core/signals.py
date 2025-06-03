from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from .models import UsuarioSistema

@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    username = "admin"
    password = "admin123"
    email = "admin@example.com"

    if not User.objects.filter(username=username).exists():
        print("Criando superusuário padrão...")
        User.objects.create_superuser(username=username, password=password, email=email)

@receiver(post_migrate)
def create_default_usuario_sistema(sender, **kwargs):
    cpf = "12345678900"
    senha = "senha123"
    email = "usuario@example.com"
    nome = "Usuário Padrão"
    
    if not UsuarioSistema.objects.filter(cpf=cpf).exists():
        UsuarioSistema.objects.create(
            nome=nome,
            email=email,
            cpf=cpf,
            senha=make_password(senha),
            endereco="Endereço padrão",
            data_nascimento="2000-01-01",
            telefone="11999999999",
            role="usuario",
            is_approved=True,
        )
        print("Usuário padrão do app criado com sucesso.")