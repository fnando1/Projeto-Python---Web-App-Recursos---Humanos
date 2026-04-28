from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("funcionarios/", views.funcionario_list, name="funcionario_list"),
    path("funcionarios/novo/", views.funcionario_create, name="funcionario_create"),
    path("funcionarios/<int:pk>/", views.funcionario_detail, name="funcionario_detail"),
    path("funcionarios/<int:pk>/editar/", views.funcionario_update, name="funcionario_update"),
    path("funcionarios/<int:pk>/excluir/", views.funcionario_delete, name="funcionario_delete"),
    path("departamentos/novo/", views.departamento_create, name="departamento_create"),
    path("er-diagram/", views.er_diagram, name="er_diagram"),
]
