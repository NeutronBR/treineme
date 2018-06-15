from mail import envia_email_template
import re


# enviar email depois de salvar um anúncio
def post_save_anuncio(sender, instance, created, **kwargs):
    # import pdb
    # pdb.set_trace()

    # import dentro da função para não incorrer em dependência circular, pois o model já importa o signals
    from cursos.models import Inscricao
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


def pre_save_video(sender, instance, *args, **kwargs):
    # extrair o id do vídeo no YouTube dada uma url
    regex = r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
    match = re.search(regex, instance.link)

    # import pdb
    # pdb.set_trace()

    if (match and len(match.group(0)) == 11):
        instance.link = match.group(0)
