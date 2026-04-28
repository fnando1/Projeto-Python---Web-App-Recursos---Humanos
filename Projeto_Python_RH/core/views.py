from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Funcionario, Departamento
from .forms import FuncionarioForm, DepartamentoForm


def dashboard(request):
    """Exibe o painel com resumo dos funcionários e departamentos."""
    total_funcionarios = Funcionario.objects.count()
    total_folha = Funcionario.objects.aggregate(total=Sum("salario"))["total"] or 0
    departamentos = Departamento.objects.order_by("nome")
    funcionarios = Funcionario.objects.select_related("departamento").order_by("nome")
    context = {
        "total_funcionarios": total_funcionarios,
        "total_folha": total_folha,
        "departamentos": departamentos,
        "funcionarios": funcionarios,
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


def funcionario_create(request):
    """Cria um novo funcionário."""
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Funcionário criado com sucesso!")
                return redirect("core:funcionario_list")
            except ValidationError as e:
                messages.error(request, f"Erro ao criar funcionário: {e.message}")
    else:
        form = FuncionarioForm()
    return render(request, "core/funcionario_form.html", {"form": form, "titulo": "Novo Funcionário"})


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


def er_diagram(request):
    """Exibe o diagrama ER do sistema."""
    return render(request, "core/er_diagram.html")
