from django.db import models

# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

class CursoManager(models.Manager):
    # pesquisa mais aprimorada
    def pesquisa(self, query):
        # icontains -> case insensitive containment test
        return self.get_queryset().filter(models.Q(nome__icontains=query) | models.Q(descricao__icontains=query))

class Curso(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    atalho = models.SlugField(unique=True, blank=False, null=False)
    instrutor = models.CharField('Nome do instrutor', max_length=100, blank=False)
    descricao = models.TextField('Descrição curta do curso', blank=False)
    sobre = models.TextField('Descrição completa do curso', blank=True)
    keywords = models.TextField('Palavras-chave', blank=True)
    categoria = models.ForeignKey(Categoria, models.SET_NULL, null=True, blank=False)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    objects = CursoManager()

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        pass
        from django.urls import reverse
        from cursos.views import detalhes
        # (URL, argumentos não nomeáveis, argumentos nomeáveis)
        # return('detalhes', (), {'atalho_curso': self.atalho})
        return reverse(detalhes, args=[str(self.atalho)])

    def get_aulas(self):
        pass
        return self.aulas.all()

    class Meta:
        # nome "mais tragável" para ser usado em alguns lugares tipo o admin
        # https://docs.djangoproject.com/en/1.11/topics/db/models/#meta-options
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nome']
