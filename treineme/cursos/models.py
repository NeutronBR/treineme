from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager
from cursos.signals import pre_save_video, post_save_anuncio
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

    tags = TaggableManager()

    objects = CursoManager()

    def __str__(self):
        return self.nome

    # @models.permalink # deprecated
    # outra forma de criar links para o curso
    def get_absolute_url(self):
        # from cursos import views
        # (URL, argumentos não nomeáveis, argumentos nomeáveis)
        # return('detalhes', (), {'atalho_curso': self.atalho})

        # (This is discouraged because you can't reverse namespaced views this way.)
        # return reverse(views.detalhes, args=[str(self.atalho)]) # outra forma
        return reverse('cursos:anuncios', args=[str(self.atalho)])


    def get_aulas(self):
        return self.aulas.all()

    class Meta:
        # nome "mais tragável" para ser usado em alguns lugares tipo o admin
        # https://docs.djangoproject.com/en/1.11/topics/db/models/#meta-options
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nome']


class Aula(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=100)
    descricao = models.TextField(verbose_name='Descrição', blank=True)
    ordem = models.IntegerField('Número de ordem', blank=True, default=0)
    curso = models.ForeignKey(Curso, verbose_name='Curso', related_name='aulas', on_delete=models.PROTECT)
    atividade = models.BooleanField(verbose_name='Vincular ao término da unidade?', default=False)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def __str__(self):
        return self.nome

    @staticmethod
    def ultima_ordem(curso):
        num = Aula.objects.filter(curso=curso).latest()
        if not num:
            return 1
        else:
            return num + 1

    def aula_prox(self):
        prox = Aula.objects.filter(curso=self.curso).filter(ordem__gt=self.ordem)
        if prox:
            return prox.first()
        else:
            return False

    def aula_ant(self):
        ant = Aula.objects.filter(curso=self.curso).filter(ordem__lt=self.ordem)
        if ant:
            return ant.last()
        else:
            return False

    def get_absolute_url(self):
        return reverse('cursos:aula_detalhes', args=[str(self.curso.atalho), str(self.pk)])

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['curso', 'ordem']
        get_latest_by = ['curso', 'ordem']
        unique_together = (('curso', 'ordem'))


class Video(models.Model):
    titulo = models.CharField(verbose_name='Título', max_length=100)
    link = models.CharField(verbose_name='ID do vídeo no YouTube', blank=True, max_length=150, help_text="Insira aqui o link completo para o vídeo no YouTube")
    arquivo = models.FileField(upload_to='aulas/videos', blank=True, null=True)
    aula = models.ForeignKey(Aula, verbose_name='Aula', related_name='videos', on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def is_embedded(self):
        return bool(self.link)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('cursos:video_detalhes', args=[str(self.aula.curso.atalho), str(self.pk)])

    class Meta:
        verbose_name = 'Vídeo'
        verbose_name_plural = 'Vídeos'


class MaterialComplementar(models.Model):
    titulo = models.CharField(verbose_name='Título', max_length=100)
    arquivo = models.FileField(upload_to='aulas/materiais_complementares')
    aula = models.ForeignKey(Aula, verbose_name='Aula', related_name='complementares', on_delete=models.PROTECT)

    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Material complementar'
        verbose_name_plural = 'Materiais complementares'


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

    videos_assistidos = models.ManyToManyField(Video, blank=True)

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


class Questao(models.Model):
    aula = models.ForeignKey(Aula, related_name='questoes', on_delete=models.PROTECT)
    enunciado = models.TextField(verbose_name='Questão', blank=False)
    disponivel = models.BooleanField('Disponível', default=True)

    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def __str__(self):
        return self.enunciado

    def prox_questao(self):
        queryset = Questao.objects.filter(aula=self.aula)
        for i, questao in enumerate(queryset):
            if (questao == self) and (self != queryset.last()):
                return queryset[i + 1]

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['aula', 'data_atualizacao']


class Alternativa(models.Model):
    texto = models.CharField(max_length=100, blank=False)
    questao = models.ForeignKey(Questao, related_name="alternativas", on_delete=models.PROTECT)
    correta = models.BooleanField('Correta?', default=False)

    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'
        ordering = ['?']


class Resposta(models.Model):
    # Matrícula respondendo ao questionário da aula
    inscricao = models.ForeignKey(Inscricao, related_name='respostas', on_delete=models.PROTECT)
    questao = models.ForeignKey(Questao, related_name='respostas', on_delete=models.PROTECT)
    enunciado = models.TextField('Enunciado', blank=False)
    alternativa_escolhida = models.CharField('Alternativa selecionada', max_length=100, blank=False)
    acerto = models.BooleanField('Acertou', default=False)

    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def __str__(self):
        return self.enunciado

    @staticmethod
    def ultima_reposta(aula, usuario):
        return(Resposta.objects.filter(
            questao__aula=aula,
            inscricao=Inscricao.objects.get(curso=aula.curso, usuario=usuario)
        ).last())


    @staticmethod
    def pontuacao_questionario(aula, usuario):
        inscricao = Inscricao.objects.get(usuario=usuario, curso=aula.curso)
        respostas = Resposta.objects.filter(inscricao=inscricao, acerto=True, questao__aula=aula).count()
        return(respostas)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['inscricao', 'data_atualizacao']
        unique_together = ('inscricao', 'questao')


class Anuncio(models.Model):
    curso = models.ForeignKey(Curso, verbose_name='Curso', on_delete=models.PROTECT, related_name='anuncios')
    titulo = models.CharField(verbose_name='Título', max_length=100)
    conteudo = models.TextField(verbose_name='Conteúdo')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('cursos:anuncio_detalhes', args=[str(self.curso.atalho), self.pk])

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-data_atualizacao']


class Comentario(models.Model):
    anuncio = models.ForeignKey(Anuncio, related_name='comentarios', on_delete=models.PROTECT)
    usuario = models.ForeignKey(get_user_model(), related_name='comentarios', on_delete=models.PROTECT)
    comentario = models.TextField(verbose_name='Comentário')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['data_criacao']



models.signals.post_save.connect(post_save_anuncio, sender=Anuncio, dispatch_uid='post_save_anuncio')
models.signals.pre_save.connect(pre_save_video, sender=Video, dispatch_uid='pre_save_video')
