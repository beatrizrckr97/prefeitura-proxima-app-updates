from django.shortcuts import render, redirect
from core.models import Chamado
def home(request):
    chamados = Chamado.objects.all().order_by('-id')  # Busca do banco
    return render(request, 'core/home.html', {'chamados': chamados})

def novo_chamado(request):
    if request.method == 'POST':
        nome = request.POST.get('name')
        endereco = request.POST.get('address')
        categoria = request.POST.get('category')
        relato = request.POST.get('report')

        # Salva no banco
        Chamado.objects.create(
            nome=nome,
            endereco=endereco,
            categoria=categoria,
            relato=relato,
            status='Em andamento'  # ou outro valor padrão
        )

        return redirect('home')

    return render(request, 'core/novo_chamado.html')