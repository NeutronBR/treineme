from django.urls import path
from cursos.views import index, cursos, detalhes, inscricao, anuncios

# app_name = namespace
app_name = 'cursos'
urlpatterns = [
    path('', index, name='index'),
    path('cursos', cursos, name='cursos'),
    path('curso/<slug:atalho_curso>', detalhes, name='detalhes'),
    path('curso/<slug:atalho_curso>/inscrever/', inscricao, name='inscricao'),
    path('curso/<slug:atalho_curso>/anuncios', anuncios, name='anuncios'),
]
