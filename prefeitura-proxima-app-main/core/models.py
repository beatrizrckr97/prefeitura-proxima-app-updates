from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class RequisicaoServico(models.Model):
    nome_cidadao = models.CharField(max_length=100)
    email = models.EmailField()
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    descricao_requisicao = models.TextField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_cidadao} - {self.servico.nome}"
