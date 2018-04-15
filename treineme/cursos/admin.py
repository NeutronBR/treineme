from django.contrib import admin
from cursos.models import Curso, Categoria
# Register your models here.


class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'atalho', 'data_criacao', 'data_atualizacao']
    search_fields = ['nome', 'atalho']
    prepopulated_fields = {'atalho': ('nome',)}


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'id', ]
    search_fields = ['nome']



admin.site.register(Curso, CursoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
