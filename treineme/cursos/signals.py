from cursos.models import Inscricao
from mail import envia_email_template


def post_save_anuncio(sender, instance, created, **kwargs):
    # import pdb
    # pdb.set_trace()
    if created:
        assunto = instance.titulo
        contexto = {
            'anuncio': instance
        }
        template_name = 'anuncio_mail.html'
        inscricoes = Inscricao.objects.filter(curso=instance.curso, status=Inscricao.INSCRITO_STATUS)

        for inscricao in inscricoes:
            lista_destinatarios = [inscricao.usuario.email]
            envia_email_template(assunto, template_name, contexto, lista_destinatarios)
