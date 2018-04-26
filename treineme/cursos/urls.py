from django.urls import path
from .views import index, cursos, detalhes

# app_name = namespace
app_name = 'cursos'
urlpatterns = [
    path('', index, name='index'),
    path('cursos', cursos, name='cursos'),
    path('curso/<slug:atalho_curso>', detalhes, name='detalhes'),
]
