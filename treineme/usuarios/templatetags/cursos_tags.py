from django.template import Library
from cursos.models import Inscricao

register = Library()

# inclusion_tag tem um template montado para retornar. HTML fixo na template. Para templates complexos que são mais fixos
# A chamada é {% meus_cursos usuario %}


@register.inclusion_tag('templatetags/meus_cursos.html')
def meus_cursos(usuario):
    inscricoes = Inscricao.objects.filter(usuario=usuario).order_by('curso')
    contexto = {
        'inscricoes': inscricoes
    }
    return contexto


# simple_tag é, basicamente, para retornar dados (contexto) desejados. O HTML será criado dentro da template que o chama, diferente da tag acima. O HTML fica mais flexível, pois o contexto está disponível na template para usar como quiser, mudando a template ou usando em vários locais.
# chamada {% meus_cursos as inscricoes %}
# https://docs.djangoproject.com/pt-br/2.0/howto/custom-template-tags/
@register.simple_tag
def load_meus_cursos(usuario):
    return Inscricao.objects.filter(usuario=usuario)
