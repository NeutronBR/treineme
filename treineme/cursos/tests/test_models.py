from django.test import TestCase
from django.test.client import Client  # simulador de navegador

from model_mommy import mommy

from cursos.models import Curso


class CursoManagerTestCase(TestCase):
    def setUp(self):
        self.cursos_django = mommy.make(
            'cursos.Curso', nome='Mundo dominado com Python', _quantity=7
        )
        self.cursos_direito = mommy.make(
            _model='cursos.Curso', nome='Direito Constitucional dominado', _quantity=8
        )
        self.cliente = Client()

    def tearDown(self):
        pass
        # Curso.objects.all().delete()

    def test_curso_consulta(self):
        consulta = Curso.objects.pesquisa('python')
        self.assertEqual(len(consulta), 7)
        consulta = Curso.objects.pesquisa('direito')
        self.assertEqual(len(consulta), 8)
        consulta = Curso.objects.pesquisa('dominado')
        self.assertEqual(len(consulta), 15)
