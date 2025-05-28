from django.shortcuts import render, redirect
from .models import Solicitacao
from .forms import SolicitacaoForm
from django.contrib.auth.decorators import login_required

def lista_solicitacoes(request):
    solicitacoes = Solicitacao.objects.all().order_by('-data_criacao')
    return render(request, 'solicitacoes/lista.html', {'solicitacoes': solicitacoes})

@login_required
def nova_solicitacao(request):
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.autor = request.user
            solicitacao.save()
            return redirect('lista_solicitacoes')
    else:
        form = SolicitacaoForm()
    return render(request, 'solicitacoes/nova.html', {'form': form})
