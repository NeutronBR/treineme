from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from usuarios.forms import RegistroForm
from django.contrib.auth.decorators import login_required

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
            # pdb.set_trace()
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
