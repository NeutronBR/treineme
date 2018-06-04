from django.contrib import admin

from forum.models import Topico, Resposta

# Register your models here.


class TopicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'data_criacao', 'data_atualizacao']
    search_fields = ['titulo', 'autor__email', 'body']


class RespostaAdmin(admin.ModelAdmin):
    list_display = ['topico', 'autor', 'data_criacao', 'data_atualizacao']
    search_fields = ['topico__title', 'autor__email', 'mensagem']


admin.site.register(Topico, TopicoAdmin)
admin.site.register(Resposta, RespostaAdmin)
