import re
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Chamado
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import UsuarioSistema
from .decorators import login_required

def login(request):
    """
    Autentica o usuário com base no CPF e senha.
    Inicia uma sessão se as credenciais estiverem corretas.
    """
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').strip()
        senha = request.POST.get('senha', '').strip()
        cpf = re.sub(r'\D', '', cpf)

        try:
            usuario = UsuarioSistema.objects.get(cpf=cpf)
            if not usuario.is_approved:
                messages.error(request, 'Seu cadastro está aguardando aprovação do administrador.')
                return render(request, 'core/login.html')

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
    """
    Encerra a sessão atual do usuário e redireciona para a tela de login.
    """
    request.session.flush()
    return redirect('login')

@login_required
def home(request):
    """
    Exibe a página inicial com a lista de chamados ordenados por ID.
    """
    chamados = Chamado.objects.all().order_by('-id')
    return render(request, 'core/home.html', {'chamados': chamados})

@login_required
def novo_chamado(request):
    """
    Permite que um usuário crie um novo chamado através de um formulário.
    """
    if request.method == 'POST':
        nome = request.POST.get('name')
        endereco = request.POST.get('address')
        categoria = request.POST.get('category')
        relato = request.POST.get('report')

        Chamado.objects.create(
            nome=nome,
            endereco=endereco,
            categoria=categoria,
            relato=relato,
            status='Em andamento'
        )

        return redirect('home')

    return render(request, 'core/novo_chamado.html')

@login_required
def ver_chamado(request, chamado_id):
    """
    Exibe os detalhes de um chamado específico.
    """
    chamado = get_object_or_404(Chamado, id=chamado_id)
    return render(request, 'core/ver_chamado.html', {'chamado': chamado})

@login_required
def editar_chamado(request, chamado_id):
    """
    Permite editar os dados de um chamado existente.
    """
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
    """
    Permite a exclusão de um chamado após confirmação.
    """
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        chamado.delete()
        return redirect('home')

    return render(request, 'core/excluir_chamado.html', {'chamado': chamado})

def cadastro(request):
    """
    Realiza o cadastro de um novo usuário comum, com validações de CPF,
    senha, nome e e-mail. Após o cadastro, aguarda aprovação do administrador.
    """
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        cpf_raw = request.POST.get('cpf', '').strip()
        senha_raw = request.POST.get('senha', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        data_nascimento = request.POST.get('data_nascimento', '').strip()
        telefone_raw = request.POST.get('telefone', '').strip()

        cpf = re.sub(r'\D', '', cpf_raw)
        telefone = re.sub(r'\D', '', telefone_raw)

        if not nome.replace(" ", "").isalpha():
            messages.error(request, 'Nome deve conter apenas letras.')
            return redirect('cadastro')

        if len(cpf) != 11:
            messages.error(request, 'CPF inválido. Informe um número com 11 dígitos.')
            return redirect('cadastro')

        if UsuarioSistema.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado.')
            return redirect('cadastro')

        if UsuarioSistema.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return redirect('cadastro')

        if len(senha_raw) < 8 or not any(char.isdigit() for char in senha_raw):
            messages.error(request, 'A senha deve conter no mínimo 8 caracteres e pelo menos um número.')
            return redirect('cadastro')

        senha = make_password(senha_raw)

        UsuarioSistema.objects.create(
            nome=nome,
            email=email,
            cpf=cpf,
            senha=senha,
            endereco=endereco,
            data_nascimento=data_nascimento,
            telefone=telefone,
            role='usuario'
        )

        messages.success(request, 'Cadastro realizado com sucesso! Aguarde aprovação do administrador.')
        return redirect('login')

    return render(request, 'core/cadastro.html')
