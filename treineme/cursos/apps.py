from django.apps import AppConfig

from django.db.models.signals import post_save


class CursosConfig(AppConfig):
    name = 'cursos'

    def ready(self):

        # import pdb
        # pdb.set_trace()
        # print('Hello')

        from cursos.models import Anuncio
        from cursos.signals import post_save_anuncio

        # post_save.connect(post_save_anuncio, sender=Anuncio, dispatch_uid='post_save_anuncio')
