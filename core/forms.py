from django import forms
from django.core.exceptions import ValidationError
from .models import Funcionario, Departamento, Ferias
import re


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "cpf", "cargo", "salario", "data_admissao", "departamento"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome completo"}),
            "cpf": forms.TextInput(attrs={"class": "form-control", "placeholder": "XXX.XXX.XXX-XX"}),
            "cargo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Desenvolvedor"}),
            "salario": forms.NumberInput(attrs={
                "class": "form-control", 
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00"
            }),
            "data_admissao": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "departamento": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "")
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        if len(cpf_limpo) != 11:
            raise ValidationError("CPF deve conter exatamente 11 dígitos.")
        
        if cpf_limpo == cpf_limpo[0] * 11:
            raise ValidationError("CPF inválido: todos os dígitos são iguais.")
        
        return cpf

    def clean_salario(self):
        salario = self.cleaned_data.get("salario")
        if salario and salario < 0:
            raise ValidationError("O salário não pode ser negativo.")
        return salario

    def clean_nome(self):
        nome = self.cleaned_data.get("nome", "").strip()
        if len(nome) < 3:
            raise ValidationError("O nome deve ter no mínimo 3 caracteres.")
        return nome


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ["nome", "sigla"]
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Recursos Humanos"
            }),
            "sigla": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: RH",
                "maxlength": "10"
            }),
        }

    def clean_sigla(self):
        sigla = self.cleaned_data.get("sigla", "").upper().strip()
        if len(sigla) < 2:
            raise ValidationError("A sigla deve ter no mínimo 2 caracteres.")
        return sigla

    def clean_nome(self):
        nome = self.cleaned_data.get("nome", "").strip()
        if len(nome) < 3:
            raise ValidationError("O nome deve ter no mínimo 3 caracteres.")
        return nome


class FeriasForm(forms.ModelForm):
    class Meta:
        model = Ferias
        fields = ["funcionario", "data_inicio", "data_fim"]
        widgets = {
            "funcionario": forms.Select(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_fim": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        if data_inicio and data_fim:
            if data_fim <= data_inicio:
                raise ValidationError("A data de término deve ser após a data de início.")
            
            dias_ferias = (data_fim - data_inicio).days
            if dias_ferias > 30:
                raise ValidationError("O período de férias não pode exceder 30 dias.")
        
        return cleaned_data
