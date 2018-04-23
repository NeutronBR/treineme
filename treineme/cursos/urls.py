from django.urls import path
from . import views

# app_name = namespace
app_name = 'cursos'
urlpatterns = [
    path('', views.index, name='index'),
    path('cursos', views.cursos, name='cursos'),
    path('curso/<slug:atalho_curso>', views.detalhes, name='detalhes'),
]
