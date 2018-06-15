from django.urls import path
from django.conf import settings
from cursos.views import index, cursos, detalhes, inscricao, anuncios, anuncio_detalhes, aulas, aula_detalhes, video_detalhes, questionario

# app_name = namespace
app_name = 'cursos'
urlpatterns = [
    path('', index, name='index'),
    path('cursos', cursos, name='cursos'),
    path('curso/<slug:atalho_curso>', detalhes, name='detalhes'),
    path('curso/<slug:atalho_curso>/inscrever', inscricao, name='inscricao'),
    path('curso/<slug:atalho_curso>/anuncios', anuncios, name='anuncios'),
    path('curso/<slug:atalho_curso>/anuncio/<int:pk>', anuncio_detalhes, name='anuncio_detalhes'),
    path('curso/<slug:atalho_curso>/aulas', aulas, name='aulas'),
    path('curso/<slug:atalho_curso>/aula/<int:aula_pk>', aula_detalhes, name='aula_detalhes'),
    path('curso/<slug:atalho_curso>/video/<int:video_pk>', video_detalhes, name='video_detalhes'),
    path('curso/<slug:atalho_curso>/aula/<int:aula_pk>/questionario', questionario, name='questionario'),
]
