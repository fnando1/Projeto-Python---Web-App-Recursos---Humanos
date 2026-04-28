from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("funcionarios/", views.funcionario_list, name="funcionario_list"),
    path("funcionarios/<int:pk>/", views.funcionario_detail, name="funcionario_detail"),
    path("funcionarios/<int:pk>/editar/", views.funcionario_update, name="funcionario_update"),
    path("funcionarios/<int:pk>/excluir/", views.funcionario_delete, name="funcionario_delete"),
    path("departamentos/novo/", views.departamento_create, name="departamento_create"),
    path("ferias/", views.ferias_list, name="ferias_list"),
    path("ferias/<int:pk>/", views.ferias_detail, name="ferias_detail"),
    path("ferias/<int:pk>/editar/", views.ferias_update, name="ferias_update"),
    path("ferias/<int:pk>/excluir/", views.ferias_delete, name="ferias_delete"),
]
