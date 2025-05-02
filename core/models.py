from django.db import models

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