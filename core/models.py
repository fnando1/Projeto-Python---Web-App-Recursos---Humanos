from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
import re

def validar_cpf(cpf):
    """Valida o CPF no formato XXX.XXX.XXX-XX ou XXXXXXXXXXX"""
    cpf_limpo = re.sub(r'\D', '', cpf)
    if len(cpf_limpo) != 11:
        raise ValidationError("CPF deve conter 11 dígitos.")
    if cpf_limpo == cpf_limpo[0] * 11:  # todos os dígitos iguais
        raise ValidationError("CPF inválido.")

def validar_salario(value):
    """Valida que o salário é positivo"""
    if value < 0:
        raise ValidationError("O salário não pode ser negativo.")

def validar_data_admissao(value):
    """Valida que a data de admissão não é no futuro"""
    if value > date.today():
        raise ValidationError("A data de admissão não pode ser no futuro.")

class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome do departamento")
    sigla = models.CharField(max_length=10, unique=True, help_text="Sigla do departamento (ex: RH, TI)")

    class Meta:
        ordering = ['nome']
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Funcionario(models.Model):
    nome = models.CharField(max_length=120)
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        validators=[validar_cpf],
        help_text="CPF no formato XXX.XXX.XXX-XX"
    )
    cargo = models.CharField(max_length=80)
    salario = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[validar_salario],
        help_text="Salário mensal em reais"
    )
    data_admissao = models.DateField(
        validators=[validar_data_admissao],
        help_text="Data de admissão"
    )
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)

    class Meta:
        ordering = ['nome']
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome


class Ferias(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name="ferias")
    data_inicio = models.DateField(help_text="Data de início das férias")
    data_fim = models.DateField(help_text="Data de término das férias")

    class Meta:
        ordering = ['-data_inicio']
        verbose_name = "Férias"
        verbose_name_plural = "Férias"

    def clean(self):
        """Validação de datas"""
        if self.data_fim <= self.data_inicio:
            raise ValidationError("A data de término deve ser após a data de início.")

    def __str__(self):
        return f"Férias de {self.funcionario.nome}: {self.data_inicio} a {self.data_fim}"
