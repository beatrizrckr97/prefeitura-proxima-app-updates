from django.shortcuts import render, redirect
from core.models import Chamado
from django.shortcuts import get_object_or_404
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        if cpf == '123' and senha == '123':
            return redirect('home') 
        else:
            messages.error(request, 'CPF ou senha inválidos.')
            return redirect('login')

    return render(request, 'core/login.html')

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

def ver_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    return render(request, 'core/ver_chamado.html', {'chamado': chamado})

def editar_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        chamado.nome = request.POST.get('name')
        chamado.endereco = request.POST.get('address')
        chamado.categoria = request.POST.get('category')
        chamado.relato = request.POST.get('report')
        chamado.save()
        return redirect('ver_chamado', chamado_id=chamado.id)

    return render(request, 'core/editar_chamado.html', {'chamado': chamado})

def excluir_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        chamado.delete()
        return redirect('home')

    return render(request, 'core/excluir_chamado.html', {'chamado': chamado})

# --- View de Cadastro ---
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        senha = request.POST.get('senha', '').strip()

        # Validação de nome apenas com letras
        if not nome.replace(" ", "").isalpha():
            messages.error(request, 'Nome deve conter apenas letras.')
            return redirect('cadastro')


        # Validação de CPF e senha igual a "123"
        if cpf != '123' or senha != '123':
            messages.error(request, 'CPF e senha devem ser "123" para acesso.')
            return redirect('cadastro')

        # Se passou, redireciona para login
        messages.success(request, 'Cadastro realizado com sucesso! Faça o login.')
        return redirect('login')

    return render(request, 'core/cadastro.html')