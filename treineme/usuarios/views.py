from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from usuarios.forms import RegistroForm, EditarUsuarioForm, ResetSenhaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from usuarios.models import SenhaReset
from cursos.models import Inscricao


# import pdb

# Create your views here.


Usuario = get_user_model()


def registrar(request):
    # pdb.set_trace()
    template_name = 'registrar.html'
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.salvar()
            usuario = authenticate(username=usuario.username, password=form.cleaned_data['password1'])
            login(request, usuario)
            return redirect('cursos:index')
    else:
        form = RegistroForm()
    contexto = {
        'formulario': form
    }
    return render(request, template_name, contexto)


def reset_senha(request):
    template_name = 'reset_senha.html'
    contexto = {}
    # se o POST estiver vazio, é a mesma coisa que form = ResetSenhaForm()
    form = ResetSenhaForm(request.POST or None)
    if form.is_valid():
        form.save()
        contexto['sucesso'] = True

    contexto['formulario'] = form
    return render(request, template_name, contexto)


def reset_senha_confirmacao(request, chave):
    template_name = 'reset_senha_confirmacao.html'
    contexto = {}
    reset = get_object_or_404(SenhaReset, chave=chave)
    # usando form padrão do django que herda de forms.Form. 'data' é conferido por is_bound
    form = SetPasswordForm(user=reset.usuario, data=request.POST or None)
    if form.is_valid():
        form.save()
        contexto['sucesso'] = True

    contexto['formulario'] = form
    return render(request, template_name, contexto)


@login_required
def painel(request):
    template_name = 'painel.html'
    contexto = {
        'inscricoes': Inscricao.objects.filter(usuario=request.user)
    }
    return render(request, template_name, contexto)


@login_required
def editar(request):
    template_name = 'editar.html'
    contexto = {}

    # if request.method == 'POST':
    form = EditarUsuarioForm(request.POST or None, instance=request.user)
    # pdb.set_trace()
    if form.is_valid():
        form.save()
        form = EditarUsuarioForm(instance=request.user)
        messages.success(request, 'Você editou sua conta com sucesso')
        contexto['sucesso'] = True
        return redirect('usuarios:painel')  # Com este redirect o contexto sucesso não está sendo usado
    # else:
        # form = EditarUsuarioForm(instance=request.user)

    contexto['formulario'] = form
    return render(request, template_name, contexto)


@login_required
def editar_senha(request):
    # usando formulário padrão do django
    template_name = 'editar_senha.html'
    contexto = {}

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            contexto['sucesso'] = True
            # para reautenticar usuário após troca de edita_senha
            update_session_auth_hash(request, form.user)
    else:
        form = PasswordChangeForm(user=request.user)

    contexto['formulario'] = form

    return render(request, template_name, contexto)
