from django.shortcuts import render, get_object_or_404, redirect
from cursos.models import Curso, Inscricao
from cursos.forms import ContatoCurso
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.http import HttpResponse

# Create your views here.


def index(request):
    # return HttpResponse('Hello world!')
    contexto = {
    }
    return render(request, 'index.html', contexto)


def cursos(request):
    contexto = {
        'cursos': Curso.objects.all()
    }
    return render(request, 'cursos.html', contexto)


def detalhes(request, atalho_curso):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    contexto = {}
    formulario = ContatoCurso(request.POST or None)
    if formulario.is_valid():
        contexto['sucesso'] = True
        formulario.envia_email(curso)
        formulario = ContatoCurso()

    contexto['formulario'] = formulario
    contexto['curso'] = curso
    return render(request, 'curso_detalhes.html', contexto)


@login_required
def inscricao(request, atalho_curso):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    # get_or_create retorna uma tupla (inscrição e True/False)
    inscricao, criado = Inscricao.objects.get_or_create(usuario=request.user, curso=curso)

    if criado:
        messages.success(request, 'Você foi inscrito(a) no curso {} com sucesso'.format(curso))
    else:
        messages.warning(request, 'Você já está inscrito(a) no curso {}'.format(curso))

    return redirect('usuarios:painel')
    # return redirect(reverse('anuncios', kwargs={'atalho_curso': atalho_curso}))
