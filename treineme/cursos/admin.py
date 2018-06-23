from django.contrib import admin
from cursos.models import Curso, Categoria, Inscricao, Anuncio, Comentario, Aula, Video, MaterialComplementar, Questao, Alternativa, Resposta
# Register your models here.


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1
    show_change_link = True


class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'atalho', 'categoria', ]
    readonly_fields = ['data_criacao', 'data_atualizacao']
    search_fields = ['nome', 'atalho']
    prepopulated_fields = {'atalho': ('nome',)}
    inlines = [AulaInline]


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'id', ]
    search_fields = ['nome']


class InscricaoAdmin(admin.ModelAdmin):
    list_display = ['curso', 'usuario', 'status']
    search_fields = ['usuario__username', 'curso__nome']
    list_filter = ['usuario', 'status', 'curso']


# class VideoInlineAdmin(admin.StackedInline):
class VideoInlineAdmin(admin.TabularInline):
    model = Video
    extra = 1



class ComplementarInlineAdmin(admin.TabularInline):
    model = MaterialComplementar
    extra = 1


class QuestaoInline(admin.TabularInline):
    model = Questao
    fields = ['enunciado', 'disponivel']
    extra = 1
    show_change_link = True


class AulaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem', 'curso']
    search_fields = ['nome']
    list_filter = ['curso']
    # prepopulated_fields = {'ordem': Aula.ultima_ordem()}

    inlines = [
        VideoInlineAdmin, ComplementarInlineAdmin, QuestaoInline
    ]


class AlternativaInline(admin.TabularInline):
    model = Alternativa
    fields = ['texto', 'correta']
    extra = 1
    ordering = ['-correta', '-data_atualizacao']


class QuestaoAdmin(admin.ModelAdmin):
    readonly_fields = ['aula']
    list_display = ['enunciado']
    inlines = [AlternativaInline]
    list_filter = ['aula__curso', 'aula']


admin.site.register(Curso, CursoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Inscricao, InscricaoAdmin)
# O registro de admin não exige a criação de uma classe
admin.site.register([Anuncio, Comentario, Video, Resposta])
admin.site.register(Aula, AulaAdmin)
admin.site.register(Questao, QuestaoAdmin)
