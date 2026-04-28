from django.contrib import admin
from django.utils.html import format_html
from .models import Departamento, Funcionario, Ferias


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "sigla", "get_total_funcionarios")
    search_fields = ("nome", "sigla")
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("nome", "sigla"),
        }),
    )
    
    def get_total_funcionarios(self, obj):
        """Exibe o total de funcionários do departamento."""
        total = obj.funcionario_set.count()
        return format_html(
            '<span style="background-color: #e8f5e9; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            total
        )
    get_total_funcionarios.short_description = "Total de Funcionários"


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "cargo", "departamento", "get_salario_formatado", "data_admissao")
    list_filter = ("departamento", "data_admissao")
    search_fields = ("nome", "cpf", "cargo")
    readonly_fields = ("get_salario_bruto", "get_dias_na_empresa")
    
    fieldsets = (
        ("Dados Pessoais", {
            "fields": ("nome", "cpf"),
        }),
        ("Informações Profissionais", {
            "fields": ("cargo", "departamento", "data_admissao", "salario"),
        }),
        ("Estatísticas", {
            "fields": ("get_salario_bruto", "get_dias_na_empresa"),
            "classes": ("collapse",),
        }),
    )
    
    def get_salario_formatado(self, obj):
        """Exibe o salário formatado como moeda."""
        return format_html(
            '<span style="color: #2e7d32; font-weight: bold;">R$ {:.2f}</span>',
            obj.salario
        )
    get_salario_formatado.short_description = "Salário"
    
    def get_salario_bruto(self, obj):
        """Exibe o salário bruto anual."""
        salario_anual = obj.salario * 12
        return format_html(
            'R$ {:.2f}',
            salario_anual
        )
    get_salario_bruto.short_description = "Salário Anual"
    
    def get_dias_na_empresa(self, obj):
        """Calcula dias na empresa."""
        from datetime import date
        dias = (date.today() - obj.data_admissao).days
        return format_html(
            '{} dias ({:.1f} anos)',
            dias,
            dias / 365.25
        )
    get_dias_na_empresa.short_description = "Tempo na Empresa"


@admin.register(Ferias)
class FeriasAdmin(admin.ModelAdmin):
    list_display = ("funcionario", "data_inicio", "data_fim", "get_dias_ferias", "get_status_ferias")
    list_filter = ("data_inicio", "funcionario__departamento")
    search_fields = ("funcionario__nome",)
    readonly_fields = ("get_dias_ferias",)
    
    fieldsets = (
        ("Informações", {
            "fields": ("funcionario", "data_inicio", "data_fim", "get_dias_ferias"),
        }),
    )
    
    def get_dias_ferias(self, obj):
        """Calcula o número de dias de férias."""
        dias = (obj.data_fim - obj.data_inicio).days + 1
        return dias
    get_dias_ferias.short_description = "Dias de Férias"
    
    def get_status_ferias(self, obj):
        """Exibe o status das férias (Planejadas, Em andamento, Finalizada)."""
        from datetime import date
        hoje = date.today()
        
        if obj.data_inicio > hoje:
            status = "Planejadas"
            cor = "#FFC107"
        elif obj.data_fim < hoje:
            status = "Finalizada"
            cor = "#4CAF50"
        else:
            status = "Em Andamento"
            cor = "#2196F3"
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            cor,
            status
        )
    get_status_ferias.short_description = "Status"
