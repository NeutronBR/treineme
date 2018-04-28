from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from usuarios.forms import RegistroForm, EditarUsuarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

# import pdb

# Create your views here.


@login_required
def painel(request):
    template_name = 'painel.html'
    contexto = {}

    return render(request, template_name, contexto)


def registrar(request):
    template_name = 'registrar.html'
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario = authenticate(username=usuario.username, password=form.cleaned_data['password1'])
            login(request, usuario)
            return redirect('cursos:index')
    else:
        form = RegistroForm()
    contexto = {
        'formulario': form
    }
    return render(request, template_name, contexto)


@login_required
def editar(request):
    template_name = 'editar.html'
    contexto = {}

    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=request.user)
        # pdb.set_trace()
        if form.is_valid():
            form.save()
            form = EditarUsuarioForm(instance=request.user)
            contexto['sucesso'] = True
    else:
        form = EditarUsuarioForm(instance=request.user)

    contexto['formulario'] = form
    return render(request, template_name, contexto)


@login_required
def senha(request):
    template_name = 'senha.html'
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
