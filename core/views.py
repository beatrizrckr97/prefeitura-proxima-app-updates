from django.shortcuts import render, redirect
from core.models import Chamado
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import UsuarioSistema
from .decorators import login_required

def login(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        try:
            usuario = UsuarioSistema.objects.get(cpf=cpf)
            if check_password(senha, usuario.senha):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.nome
                request.session['usuario_role'] = usuario.role
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta.')
        except UsuarioSistema.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

    return render(request, 'core/login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

@login_required
def home(request):
    chamados = Chamado.objects.all().order_by('-id')  # Busca do banco
    return render(request, 'core/home.html', {'chamados': chamados})

@login_required
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

@login_required
def ver_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    return render(request, 'core/ver_chamado.html', {'chamado': chamado})

@login_required
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

@login_required
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