from django.urls import path
from django.contrib.auth.views import login, logout
from usuarios.views import registrar, painel, editar, editar_senha, reset_senha, reset_senha_confirmacao

# app_name = namespace
app_name = 'usuarios'
urlpatterns = [
    path('', painel, name='painel'),
    path('entrar/', login, kwargs={'template_name': 'login.html', 'redirect_authenticated_user': True, }, name='login'),
    path('cadastre-se/', registrar, name='registrar'),
    path('sair/', logout, kwargs={'next_page': 'cursos:index'}, name='logout'),
    path('editar/', editar, name='editar'),
    path('editar_senha/', editar_senha, name='editar_senha'),
    path('esqueceu_senha/', reset_senha, name='reset_senha'),
    path('nova_senha/<str:chave>', reset_senha_confirmacao, name='nova_senha'),    

]
