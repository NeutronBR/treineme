from django.db import models
from django.conf import settings

# Create your models here.


class SenhaReset(models.Model):
    # numa relação 1..N, para acessar todos os N`s do 1, basta objeto.foreignkey_set.all()
    # neste exemplo, onde o usuário já foi selecionado: usuario.senhareset_set.all()
    # e para facilictar, basta o related_name. objeto.related_name.all() usuario.resets.all()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE, related_name='resets')
    chave = models.CharField('Chave', max_length=100, unique=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    usado = models.BooleanField('Link usado', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.usuario, self.criado_em)

    class Meta:
        verbose_name = 'Nova senha'
        verbose_name_plural = 'Novas senhas'
        ordering = ['-criado_em']
