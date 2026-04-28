from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Funcionario, Departamento, Ferias
from .forms import FuncionarioForm, DepartamentoForm, FeriasForm


def dashboard(request):
    """Exibe o painel com resumo dos funcionários e departamentos."""
    hoje = date.today()
    proximo_mes = hoje + timedelta(days=30)
    
    total_funcionarios = Funcionario.objects.count()
    total_folha = Funcionario.objects.aggregate(total=Sum("salario"))["total"] or 0
    departamentos = Departamento.objects.order_by("nome")
    funcionarios = Funcionario.objects.select_related("departamento").order_by("nome")
    
    # Férias - em andamento (hoje está entre data_inicio e data_fim)
    ferias_em_andamento = Ferias.objects.filter(
        data_inicio__lte=hoje, 
        data_fim__gte=hoje
    ).select_related("funcionario")
    
    # Férias próximas (começa entre hoje e próximos 30 dias)
    ferias_proximas = Ferias.objects.filter(
        data_inicio__gt=hoje, 
        data_inicio__lte=proximo_mes
    ).select_related("funcionario").order_by("data_inicio")
    
    total_ferias_hoje = ferias_em_andamento.count()
    
    context = {
        "total_funcionarios": total_funcionarios,
        "total_folha": total_folha,
        "departamentos": departamentos,
        "funcionarios": funcionarios,
        "ferias_em_andamento": ferias_em_andamento,
        "ferias_proximas": ferias_proximas,
        "total_ferias_hoje": total_ferias_hoje,
        "hoje": hoje,
    }
    return render(request, "core/dashboard.html", context)


def funcionario_list(request):
    """Lista funcionários com filtros de busca e departamento."""
    search = request.GET.get("search", "")
    dept_id = request.GET.get("departamento", "")
    funcionarios = Funcionario.objects.select_related("departamento").all()
    
    if search:
        funcionarios = funcionarios.filter(nome__icontains=search)
    if dept_id:
        try:
            funcionarios = funcionarios.filter(departamento__id=dept_id)
        except (ValueError, TypeError):
            messages.warning(request, "Departamento inválido.")
    
    departamentos = Departamento.objects.all()
    return render(request, "core/funcionario_list.html", {
        "funcionarios": funcionarios,
        "departamentos": departamentos,
        "search": search,
        "departamento_atual": dept_id,
    })


def funcionario_detail(request, pk):
    """Exibe os detalhes de um funcionário específico."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    return render(request, "core/funcionario_detail.html", {"funcionario": funcionario})


def funcionario_update(request, pk):
    """Atualiza os dados de um funcionário."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Funcionário atualizado com sucesso!")
                return redirect("core:funcionario_detail", pk=funcionario.pk)
            except ValidationError as e:
                messages.error(request, f"Erro ao atualizar funcionário: {e.message}")
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, "core/funcionario_form.html", {"form": form, "titulo": "Editar Funcionário"})
    """Atualiza os dados de um funcionário."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Funcionário atualizado com sucesso!")
                return redirect("core:funcionario_detail", pk=funcionario.pk)
            except ValidationError as e:
                messages.error(request, f"Erro ao atualizar funcionário: {e.message}")
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, "core/funcionario_form.html", {"form": form, "titulo": "Editar Funcionário"})


def funcionario_delete(request, pk):
    """Deleta um funcionário após confirmação."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == "POST":
        try:
            funcionario.delete()
            messages.success(request, "Funcionário deletado com sucesso!")
            return redirect("core:funcionario_list")
        except ValidationError as e:
            messages.error(request, f"Erro ao deletar funcionário: {e.message}")
    return render(request, "core/funcionario_confirm_delete.html", {"funcionario": funcionario})


def departamento_create(request):
    """Cria um novo departamento."""
    if request.method == "POST":
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Departamento criado com sucesso!")
                return redirect("core:dashboard")
            except ValidationError as e:
                messages.error(request, f"Erro ao criar departamento: {e.message}")
    else:
        form = DepartamentoForm()
    return render(request, "core/departamento_form.html", {"form": form, "titulo": "Novo Departamento"})


def ferias_list(request):
    """Lista férias de todos os funcionários."""
    search = request.GET.get("search", "")
    ferias = Ferias.objects.select_related("funcionario").order_by("-data_inicio")
    
    if search:
        ferias = ferias.filter(funcionario__nome__icontains=search)
    
    return render(request, "core/ferias_list.html", {
        "ferias": ferias,
        "search": search,
    })


def ferias_detail(request, pk):
    """Exibe os detalhes de um período de férias."""
    ferias = get_object_or_404(Ferias, pk=pk)
    dias_ferias = (ferias.data_fim - ferias.data_inicio).days
    return render(request, "core/ferias_detail.html", {
        "ferias": ferias,
        "dias_ferias": dias_ferias,
    })
    """Exibe os detalhes de um período de férias."""
    ferias = get_object_or_404(Ferias, pk=pk)
    dias_ferias = (ferias.data_fim - ferias.data_inicio).days
    return render(request, "core/ferias_detail.html", {
        "ferias": ferias,
        "dias_ferias": dias_ferias,
    })


def ferias_update(request, pk):
    """Atualiza um período de férias."""
    ferias = get_object_or_404(Ferias, pk=pk)
    if request.method == "POST":
        form = FeriasForm(request.POST, instance=ferias)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Período de férias atualizado com sucesso!")
                return redirect("core:ferias_detail", pk=ferias.pk)
            except ValidationError as e:
                messages.error(request, f"Erro ao atualizar férias: {e.message}")
    else:
        form = FeriasForm(instance=ferias)
    return render(request, "core/ferias_form.html", {"form": form, "titulo": "Editar Férias"})


def ferias_delete(request, pk):
    """Deleta um período de férias após confirmação."""
    ferias = get_object_or_404(Ferias, pk=pk)
    if request.method == "POST":
        try:
            ferias.delete()
            messages.success(request, "Período de férias deletado com sucesso!")
            return redirect("core:ferias_list")
        except ValidationError as e:
            messages.error(request, f"Erro ao deletar férias: {e.message}")
    return render(request, "core/ferias_confirm_delete.html", {"ferias": ferias})
