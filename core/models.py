from django.db import models
from django.contrib.auth.hashers import make_password

class Chamado(models.Model):
    STATUS_CHOICES = [
        ('Resolvido', 'Resolvido'),
        ('Em andamento', 'Em andamento'),
    ]

    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    relato = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Em andamento')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chamado {self.id} - {self.status}'

class UsuarioSistema(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('agente', 'Agente'),
        ('usuario', 'Usuário Comum'),  # novo tipo
    ]

    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    senha = models.CharField(max_length=128)
    endereco = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='usuario')
    is_approved = models.BooleanField(default=False)  # <-- campo adicionado

    def save(self, *args, **kwargs):
        # Só criptografa se a senha não estiver já criptografada (para evitar dupla criptografia)
        if not self.senha.startswith('pbkdf2_'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.role})"