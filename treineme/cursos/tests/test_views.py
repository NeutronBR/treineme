from django.test import TestCase
from django.urls import reverse
from django.test.client import Client  # simulador de navegador
from django.core import mail
from django.conf import settings

from cursos.models import Curso

# Create your tests here.
# test_ é o início obrigatório das funcões que farão o teste


class IndexViewTest(TestCase):
    def test_index_status_code(self):
        cliente = Client()
        resposta = cliente.get(reverse('cursos:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'base.html')
        self.assertTemplateUsed(resposta, 'index.html')


class ContatoCursoTestCase(TestCase):

    # executa o setUpClass 1x para a classe
    @classmethod
    def setUpClass(cls):
        pass

    # Executa setUp antes e tearDown depois de cada teste
    def setUp(self):
        self.curso = Curso.objects.create(nome='Django', atalho='django')

    def tearDown(self):
        self.curso.delete()

    # executa ao final de todos os testes
    @classmethod
    def tearDownClass(cls):
        pass

    def test_form_contato_erro(self):
        dados = {
            'nome': 'Fulano de Tal',
            'email': '',
            'mensagem': ''
        }
        cliente = Client()
        caminho = reverse('cursos:detalhes', args=[self.curso.atalho])
        resposta = cliente.post(caminho, dados)
        self.assertFormError(resposta, 'formulario', 'email', 'Este campo é obrigatório.')
        self.assertFormError(resposta, 'formulario', 'mensagem', 'Este campo é obrigatório.')

    def teste_form_contato_sucesso(self):
        dados = {
            'nome': 'Fulano de Tal',
            'email': 'teste@teste.com',
            'mensagem': 'Olá'
        }
        cliente = Client()
        caminho = reverse('cursos:detalhes', args=[self.curso.atalho])
        resposta = cliente.post(caminho, dados)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
