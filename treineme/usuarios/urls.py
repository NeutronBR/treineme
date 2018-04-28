from django.urls import path
from django.contrib.auth.views import login, logout
from usuarios.views import registrar, painel, editar, senha

# app_name = namespace
app_name = 'usuarios'
urlpatterns = [
    path('', painel, name='painel'),
    path('entrar/', login, kwargs={'template_name': 'login.html', 'redirect_authenticated_user': True, }, name='login'),
    path('cadastre-se/', registrar, name='registrar'),
    path('sair/', logout, kwargs={'next_page': 'cursos:index'}, name='logout'),
    path('editar/', editar, name='editar'),
    path('senha/', senha, name='senha'),
]
