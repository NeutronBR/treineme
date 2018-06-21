from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from cursos.models import Curso, Inscricao


def inscricao_requerida(view_func):
    def _wrapper(request, *args, **kwargs):
        atalho_curso = kwargs['atalho_curso']
        curso = get_object_or_404(Curso, atalho=atalho_curso)
        if not request.user.is_staff:
            try:
                inscricao = Inscricao.objects.get(usuario=request.user, curso=curso)
                if not inscricao.inscrito():
                    messages.error(request, 'Sua inscrição em {} está pendente'.format(curso))
                    return redirect('usuarios:painel')
            except ObjectDoesNotExist:
                messages.warning(request, 'Você ainda não se inscreveu em {}'.format(curso))
                return redirect(reverse('cursos:detalhes', kwargs={'atalho_curso': atalho_curso}))

        return view_func(request, *args, **kwargs)
    return _wrapper
