from django.shortcuts import render, get_object_or_404, redirect, reverse
from cursos.models import Curso, Inscricao, Anuncio, Aula, Video, Questao, Resposta, Alternativa
from cursos.forms import ContatoCurso, ComentarioForm, AvaliacaoCursoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.decorators import inscricao_requerida
from django.template.defaultfilters import pluralize
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from io import BytesIO

# Create your views here.


def index(request):
    # return HttpResponse('Hello world!')
    contexto = {
    }
    return render(request, 'index.html', contexto)


def cursos(request):
    contexto = {
        'cursos': Curso.objects.all()
    }
    return render(request, 'cursos.html', contexto)


def detalhes(request, atalho_curso):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    contexto = {}
    formulario = ContatoCurso(request.POST or None)
    if formulario.is_valid():
        contexto['sucesso'] = True
        formulario.envia_email(curso)
        formulario = ContatoCurso()

    contexto['formulario'] = formulario
    contexto['curso'] = curso
    return render(request, 'curso_detalhes.html', contexto)


@login_required
def inscricao(request, atalho_curso):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    # get_or_create retorna uma tupla (inscrição e True/False)
    inscricao, criado = Inscricao.objects.get_or_create(usuario=request.user, curso=curso)

    if criado:
        messages.success(request, 'Você foi inscrito(a) no curso {} com sucesso'.format(curso))
    else:
        messages.warning(request, 'Você já está inscrito(a) no curso {}'.format(curso))

    return redirect('cursos:anuncios', curso.atalho)
    # return redirect(reverse('anuncios', kwargs={'atalho_curso': atalho_curso}))


@login_required
@inscricao_requerida
def anuncios(request, atalho_curso):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    template = 'anuncios.html'
    contexto = {
        'curso': curso,
        'anuncios': curso.anuncios.all()
    }
    return render(request, template, contexto)


@login_required
@inscricao_requerida
def anuncio_detalhes(request, atalho_curso, pk):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    # anuncio = get_object_or_404(curso.anuncios.all(), pk=pk)
    anuncio = get_object_or_404(Anuncio, pk=pk)
    form = ComentarioForm(request.POST or None)

    # print('Tipo: {}'.format(type(request)))
    # print('Dir: {}'.format(dir(request)))

    if form.is_valid():
        # atribuir ao form os dados enviados mas sem salvar no BD
        comentario = form.save(commit=False)
        comentario.anuncio = anuncio
        comentario.usuario = request.user
        # salvar efetivamente no BD
        comentario.save()

        form = ComentarioForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')

    template = "anuncio_detalhes.html"

    contexto = {
        'curso': curso,
        'anuncio': anuncio,
        'comentarios': anuncio.comentarios.all(),
        'formulario': form
    }


    return render(request, template, contexto)


@login_required
@inscricao_requerida
def aulas(request, atalho_curso):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    template = 'aulas.html'
    contexto = {
        'curso': curso,
        'aulas': curso.get_aulas()
    }
    return render(request, template, contexto)


@login_required
@inscricao_requerida
def aula_detalhes(request, atalho_curso, aula_pk):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    # aula = get_object_or_404(Aula, pk=aula_pk, curso=curso)
    aula = get_object_or_404(Aula, pk=aula_pk)
    template = 'aula_detalhes.html'
    contexto = {
        'curso': curso,
        'aula': aula,
        'videos': aula.videos.all().order_by('data_criacao'),
        'materiais_complementares': aula.complementares.all(),
        'questionario': aula.questoes.exists(),
    }
    return render(request, template, contexto)


@login_required
@inscricao_requerida
def video_detalhes(request, atalho_curso, video_pk):
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    video = get_object_or_404(Video, id=video_pk)
    template = 'video_detalhes.html'
    contexto = {
        'curso': curso,
        'video': video,
        'aula': video.aula
    }
    return render(request, template, contexto)


@login_required
@inscricao_requerida
def questionario(request, atalho_curso, aula_pk):
    template = 'questionario.html'
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    aula = get_object_or_404(Aula, pk=aula_pk)
    # Inscricao.objects.get(curso=curso, usuario=request.user).atualiza_situacao()

    contexto = {
        'curso': curso,
        'aula': aula,
        'questoes': aula.questoes.filter(disponivel=True),
        'ult_resposta': Resposta.ultima_reposta(aula, request.user),
        'pontos': Resposta.pontuacao_questionario(aula, request.user)
    }
    return render(request, template, contexto)


@login_required
@inscricao_requerida
def resposta(request, atalho_curso, aula_pk, questao_pk):

    template_name = 'questao.html'
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    aula = get_object_or_404(Aula, pk=aula_pk)
    questao = get_object_or_404(Questao, pk=questao_pk)
    inscricao = Inscricao.objects.get(usuario=request.user, curso=curso)

    # import pdb
    # pdb.set_trace()

    # form = RespostaForm(request.POST or None)
    # form.fields['alternativas'].queryset = Alternativa.objects.filter(questao=questao)
    if request.method == 'POST':
        # se o post tiver uma alternativa selecionada
        alternativa = Alternativa.objects.get(pk=request.POST.get('alternativa')) if request.POST.get('alternativa') else ''

        if alternativa:
            campos = {
                'enunciado': questao.enunciado,
                'alternativa_escolhida': alternativa.texto,
                'acerto': alternativa.correta
            }
            resposta, criado = Resposta.objects.update_or_create(inscricao=inscricao, questao=questao, enunciado=questao.enunciado, defaults=campos)

            questao = questao.prox_questao()
        else:
            messages.warning(request, 'Você deve escolher uma opção')

    contexto = {
        'curso': curso,
        'aula': aula,
        'questao': questao
    }

    inscricao.atualiza_nota()
    inscricao.atualiza_situacao()

    if questao:
        return render(request, template_name, contexto)
    else:
        respostas = Resposta.pontuacao_questionario(aula, request.user)
        messages.success(request, 'Você acertou {} quest{}'.format(respostas, pluralize(respostas, "ão,ões")))
        return redirect(reverse('cursos:aula_detalhes', kwargs={'atalho_curso': atalho_curso, 'aula_pk': aula.pk}))


@login_required
def video_assistido(request, *args, **kwargs):
    # >>>>> FAZER UMA INSCRIÇÃO REQUERIDA <<<<<
    if request.is_ajax() and request.POST:
        print(request.POST)

        try:
            inscricao = Inscricao.objects.get(usuario=request.user, curso__atalho=request.POST['atalho_curso'])
            video = Video.objects.get(pk=request.POST['video_pk'])

            inscricao.video_assistido(video)
            inscricao.videos_finalizados()
            inscricao.atualiza_situacao()
        except Exception as e:
            raise e

        data = {
            "message": "Vídeo assistido"
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound()


def relatorio_usuarios(request):
    if request.user.is_staff:
        template = 'relatorio_usuarios.html'
        usuarios = get_user_model().objects.all().order_by('first_name', 'last_name')

        contexto = {
            'usuarios': usuarios,
        }
        return render(request, template, contexto)
    else:
        return redirect('usuarios:painel')


def relatorio_cursos(request):
    if request.user.is_staff:
        template = 'relatorio_cursos.html'
        cursos = Curso.objects.all()

        contexto = {
            'cursos': cursos,
        }
        return render(request, template, contexto)
    else:
        return redirect('usuarios:painel')


@login_required
@inscricao_requerida
def informacoes(request, atalho_curso):
    template = 'informacoes.html'
    contexto = {}
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    inscricao = Inscricao.objects.get(curso=curso, usuario=request.user)
    form = AvaliacaoCursoForm(request.POST or None, instance=inscricao)

    if form.is_valid():
        form.save()
        form = AvaliacaoCursoForm(instance=inscricao)
        messages.success(request, 'Sua avaliação foi enviada com sucesso')
        contexto['sucesso'] = True


    contexto = {
        'curso': curso,
        'formulario': form,
        'inscricao': inscricao
    }
    return render(request, template, contexto)


@login_required
@inscricao_requerida
def certificado(request, atalho_curso):
    contexto = {}
    curso = get_object_or_404(Curso, atalho=atalho_curso)
    inscricao = Inscricao.objects.get(curso=curso, usuario=request.user)

    if not inscricao.aprovado():
        messages.info(request, 'Você ainda não atingiu os requisitos para emitir o certificado')
        return redirect(reverse('cursos:informacoes', kwargs={'atalho_curso': atalho_curso}))
    else:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from django.utils import formats


        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'

        buffer = BytesIO()


        aluno = inscricao.usuario.get_full_name()
        curso = str(inscricao.curso)
        # data = inscricao.data_atualizacao.strftime("%d/%B/%Y")
        data = formats.date_format(inscricao.data_atualizacao, format="DATE_FORMAT")
        empresa = settings.NOME_EMPRESA + " Treine-me"

        y, x = A4
        margem_topo = y - 15 * mm
        margem_base = 15 * mm
        margem_esquerda = 15 * mm
        margem_direita = x - 15 * mm
        altura_cabecalho = 35 * mm
        largura_util = (x - margem_esquerda - (x - margem_direita))

        string = empresa
        font = 'Times-Roman'
        size = 30

        # Create the PDF object, using the BytesIO object as its "file."
        my_canvas = canvas.Canvas(buffer)
        my_canvas.setPageSize((x, y))

        # Desenha cabeçalho cinza
        my_canvas.setFillGray(0.40)
        my_canvas.rect(margem_esquerda, (margem_topo - altura_cabecalho),
                       (x - margem_esquerda - (x - margem_direita)), altura_cabecalho,
                       stroke=0, fill=1)

        # Desenha corpo
        my_canvas.rect(margem_esquerda, margem_base,
                       largura_util,
                       (margem_topo - margem_base - altura_cabecalho - 10 * mm),
                       stroke=1, fill=0)

        # Create textobject
        textobject = my_canvas.beginText()


        # Cabeçalho
        textobject.setFont(font, size)
        texto_centralizado = ((largura_util - my_canvas.stringWidth(string, font, size)) / 2 + margem_esquerda)
        textobject.setTextOrigin(texto_centralizado,
                                 margem_topo - altura_cabecalho / 2)
        textobject.setFillColor(colors.white)
        textobject.textLine(text=string)


        # Nome Aluno
        string = aluno
        texto_centralizado = ((largura_util - my_canvas.stringWidth(string, font, size)) / 2 + margem_esquerda)
        textobject.setFillColor(colors.black)
        textobject.setTextOrigin(texto_centralizado, 320)
        textobject.textLine(text=string)

        # Curso
        string = curso
        texto_centralizado = ((largura_util - my_canvas.stringWidth(string, font, size)) / 2 + margem_esquerda)
        textobject.setFillColor(colors.black)
        textobject.setTextOrigin(texto_centralizado, 190)
        textobject.textLine(text=string)



        size = 16
        textobject.setFont(font, size)

        string = "Certificamos que"
        texto_centralizado = ((largura_util - my_canvas.stringWidth(string, font, size)) / 2 + margem_esquerda)
        textobject.setTextOrigin(texto_centralizado, 370)
        textobject.textLine(text=string)

        string = "Concluiu com êxito o curso"
        texto_centralizado = ((largura_util - my_canvas.stringWidth(string, font, size)) / 2 + margem_esquerda)
        textobject.setTextOrigin(texto_centralizado, 230)
        textobject.textLine(text=string)

        string = "Concedido em " + data
        texto_centralizado = ((largura_util - my_canvas.stringWidth(string, font, size)) / 2 + margem_esquerda)
        textobject.setTextOrigin(texto_centralizado, 90)
        textobject.textLine(text=string)

        # Write text to the canvas
        my_canvas.drawText(textobject)

        # Close the PDF object cleanly.
        my_canvas.showPage()
        my_canvas.save()

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
