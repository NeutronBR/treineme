from django.shortcuts import render, get_object_or_404
from .models import Curso
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
    contexto = {
        'curso': curso,
    }
    return render(request, 'curso_detalhes.html', contexto)
