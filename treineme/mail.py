from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def envia_email_template(assunto, template_name, contexto, lista_destinatarios, remetente=settings.DEFAULT_FROM_EMAIL, falha_silenciosa=False):
    mensagem_html = render_to_string(template_name, contexto)
    mensagem_txt = striptags(mensagem_html)

    email = EmailMultiAlternatives(subject=assunto, body=mensagem_txt, from_email=remetente, to=lista_destinatarios)
    email.attach_alternative(mensagem_html, "text/html")
    email.send(fail_silently=falha_silenciosa)
