from django.contrib import admin
from cursos.models import Curso, Categoria, Inscricao, Anuncio, Comentario
# Register your models here.


class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'atalho', 'categoria', 'data_criacao', 'data_atualizacao']
    search_fields = ['nome', 'atalho']
    prepopulated_fields = {'atalho': ('nome',)}


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'id', ]
    search_fields = ['nome']


class InscricaoAdmin(admin.ModelAdmin):
    list_display = ['curso', 'usuario', 'status']
    search_fields = ['usuario__username', 'curso__nome']



admin.site.register(Curso, CursoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Inscricao, InscricaoAdmin)
# O registro de admin não exige a criação de uma classe
admin.site.register([Anuncio, Comentario, ])
