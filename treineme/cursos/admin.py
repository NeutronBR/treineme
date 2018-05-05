from django.contrib import admin
from cursos.models import Curso, Categoria, Inscricao, Anuncio, Comentario, Aula, Video
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


# class VideoInlineAdmin(admin.StackedInline):
class VideoInlineAdmin(admin.TabularInline):
    model = Video


class AulaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem', 'curso']
    search_fields = ['nome']
    list_filter = ['curso']

    inlines = [
        VideoInlineAdmin,
    ]


admin.site.register(Curso, CursoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Inscricao, InscricaoAdmin)
# O registro de admin não exige a criação de uma classe
admin.site.register([Anuncio, Comentario, Video])
admin.site.register(Aula, AulaAdmin)
