from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from .models import Departamento, Funcionario, Ferias


class FeriasPredictionTests(TestCase):
    def setUp(self):
        self.depto = Departamento.objects.create(nome="Tecnologia", sigla="TI")
        self.func = Funcionario.objects.create(
            nome="João Teste",
            cpf="123.456.789-09",
            cargo="Analista",
            salario="3500.00",
            data_admissao=date.today() - timedelta(days=365),
            departamento=self.depto,
        )

    def test_proxima_ferias_sem_historico(self):
        proxima = self.func.get_proxima_aquisicao_ferias()
        self.assertEqual(proxima, self.func.data_admissao + timedelta(days=365))

    def test_proxima_ferias_com_historico(self):
        ultimo_periodo = Ferias.objects.create(
            funcionario=self.func,
            data_inicio=date.today() - timedelta(days=120),
            data_fim=date.today() - timedelta(days=90),
        )
        proxima = self.func.get_proxima_aquisicao_ferias()
        self.assertEqual(proxima, ultimo_periodo.data_fim + timedelta(days=365))

    def test_proxima_ferias_com_ferias_trocadas_12_dias(self):
        ultimo_periodo = Ferias.objects.create(
            funcionario=self.func,
            data_inicio=date.today() - timedelta(days=50),
            data_fim=date.today() - timedelta(days=39),
        )
        proxima = self.func.get_proxima_aquisicao_ferias()
        self.assertEqual(proxima, ultimo_periodo.data_fim + timedelta(days=353))

    def test_ferias_nao_pode_sobrepor_periodo_existente(self):
        Ferias.objects.create(
            funcionario=self.func,
            data_inicio=date.today() - timedelta(days=60),
            data_fim=date.today() - timedelta(days=30),
        )

        ferias_sobrepostas = Ferias(
            funcionario=self.func,
            data_inicio=date.today() - timedelta(days=45),
            data_fim=date.today() - timedelta(days=15),
        )

        with self.assertRaises(ValidationError):
            ferias_sobrepostas.full_clean()


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.depto = Departamento.objects.create(nome="Tecnologia", sigla="TI")
        self.func = Funcionario.objects.create(
            nome="João Teste",
            cpf="123.456.789-09",
            cargo="Analista",
            salario="3500.00",
            data_admissao=date.today() - timedelta(days=365),
            departamento=self.depto,
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Teste')

    def test_funcionario_list_view(self):
        response = self.client.get(reverse('core:funcionario_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Teste')

    def test_funcionario_detail_view(self):
        response = self.client.get(reverse('core:funcionario_detail', args=[self.func.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Teste')

    def test_funcionario_create_view_get(self):
        response = self.client.get(reverse('core:funcionario_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Novo Funcionário')

    def test_funcionario_create_view_post(self):
        data = {
            'nome': 'Maria Silva',
            'cpf': '987.654.321-00',
            'cargo': 'Desenvolvedora',
            'salario': '4500.00',
            'data_admissao': '2023-01-01',
            'departamento': self.depto.pk
        }
        response = self.client.post(reverse('core:funcionario_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Funcionario.objects.filter(nome='Maria Silva').exists())

    def test_ferias_create_view_get(self):
        response = self.client.get(reverse('core:ferias_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registrar Férias')

    def test_ferias_create_view_post(self):
        data = {
            'funcionario': self.func.pk,
            'data_inicio': '2026-07-01',
            'data_fim': '2026-07-30'
        }
        response = self.client.post(reverse('core:ferias_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Ferias.objects.filter(funcionario=self.func).exists())

    def test_departamento_create_view_post(self):
        data = {
            'nome': 'Recursos Humanos',
            'sigla': 'RH'
        }
        response = self.client.post(reverse('core:departamento_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Departamento.objects.filter(sigla='RH').exists())

