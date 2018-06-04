from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from cursos.models import Curso

# Create your models here.


class Topico(models.Model):

    titulo = models.CharField(verbose_name='Título', max_length=100)
    mensagem = models.TextField(verbose_name='Mensagem')
    autor = models.ForeignKey(get_user_model(), verbose_name='Autor', related_name='topicos', on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, verbose_name='Curso', related_name='topicos', on_delete=models.PROTECT)
    visualizacoes = models.IntegerField(verbose_name='Visualizações', default=0)
    cont_respostas = models.IntegerField(verbose_name='Respostas', default=0)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    tags = TaggableManager()

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-data_criacao']


class Resposta(models.Model):

    mensagem = models.TextField(verbose_name='Resposta')
    autor = models.ForeignKey(get_user_model(), verbose_name='Autor', related_name='respostas', on_delete=models.PROTECT)
    topico = models.ForeignKey(Topico, verbose_name='Tópico', related_name='respostas', on_delete=models.PROTECT)
    # correta = BooleanField(verbose_name='Resposta correta?', default=False)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')


    def __str__(self):
        return self.mensagem[:100]  # primeiros 100 caracteres

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        # ordering = ['-correta', 'data_criacao']
        ordering = ['data_criacao']
