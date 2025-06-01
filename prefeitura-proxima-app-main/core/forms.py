from django import forms
from .models import RequisicaoServico

class RequisicaoServicoForm(forms.ModelForm):
    class Meta:
        model = RequisicaoServico
        fields = ['nome_cidadao', 'email', 'servico', 'descricao_requisicao']
