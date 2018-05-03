from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model

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


    # @models.permalink # deprecated
    # outra forma de criar links para o curso
    def get_absolute_url(self):
        from django.urls import reverse
        # from cursos import views
        # (URL, argumentos não nomeáveis, argumentos nomeáveis)
        # return('detalhes', (), {'atalho_curso': self.atalho})

        # (This is discouraged because you can't reverse namespaced views this way.)
        # return reverse(views.detalhes, args=[str(self.atalho)]) # outra forma
        return reverse('cursos:detalhes', args=[str(self.atalho)])


    def get_aulas(self):
        pass
        return self.aulas.all()


    class Meta:
        # nome "mais tragável" para ser usado em alguns lugares tipo o admin
        # https://docs.djangoproject.com/en/1.11/topics/db/models/#meta-options
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nome']


class Inscricao(models.Model):
    PENDENTE_STATUS = 0
    INSCRITO_STATUS = 1
    APROVADO_STATUS = 2
    CANCELADO_STATUS = 3
    STATUS_CHOICES = (
        (PENDENTE_STATUS, 'Pendente'),
        (INSCRITO_STATUS, 'Inscrito'),
        (APROVADO_STATUS, 'Aprovado'),
        (CANCELADO_STATUS, 'Cancelado')
    )
    # usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='inscricoes')
    usuario = models.ForeignKey(get_user_model(), verbose_name='Usuário', related_name='inscricoes', on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, verbose_name='Curso', related_name='inscricoes', on_delete=models.PROTECT)
    status = models.IntegerField(verbose_name='Situação', choices=STATUS_CHOICES, default=INSCRITO_STATUS, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def __str__(self):
        return '{} inscrito em {}'.format(self.usuario.get_full_name(), self.curso)

    def inscrever(self):
        self.status = self.INSCRITO_STATUS
        self.save()

    def inscrito(self):
        return not(self.status == (self.PENDENTE_STATUS or self.CANCELADO_STATUS))

    def aprovado(self):
        return self.status == self.APROVADO_STATUS

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('curso', 'usuario'),)


class Anuncio(models.Model):
    curso = models.ForeignKey(Curso, verbose_name='Curso', on_delete=models.PROTECT)
    titulo = models.CharField(verbose_name='Título', max_length=100)
    conteudo = models.TextField(verbose_name='Conteúdo')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')
