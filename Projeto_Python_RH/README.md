# Projeto Python RH

Criação de sistema RH com Django + PostgreSQL ou SQLite.

## Requisitos
- Modelos:
  - Funcionario (Nome, CPF, Cargo, Salário, Data de Admissão, Departamento)
  - Departamento (Nome, Sigla)
  - Ferias (Funcionario, Data Início, Data Fim)
- Interface responsiva Bootstrap 5 com Navbar e Sidebar
- CRUD completo de funcionários
- Busca e filtro por departamento
- Dashboard com métricas

## Como rodar (Passo a Passo)

### Opção 1: Usando SQLite (Recomendado para desenvolvimento rápido)

```bash
cd /workspaces/Projeto_Python_RH
pip install -r requirements.txt
export DJANGO_USE_SQLITE=1
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Acesse em: http://localhost:8000

### Opção 2: Usando PostgreSQL

#### A) Preparar o banco PostgreSQL
No terminal do PostgreSQL (psql):

```sql
CREATE DATABASE rh_system;
```

#### B) Configurar ambiente

```bash
cd /workspaces/Projeto_Python_RH
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### C) Configurar settings.py

No `rh_system/settings.py`, configure:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rh_system',
        'USER': 'seu_usuario_postgres',
        'PASSWORD': 'sua_senha_postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### D) Migrar e rodar

```bash
python manage.py migrate
python manage.py runserver
```

No `rh_system/settings.py`, configure:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rh_system',
        'USER': 'seu_usuario_postgres',
        'PASSWORD': 'sua_senha_postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### D) Migrar e rodar

```bash
python manage.py migrate
python manage.py runserver
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### E) Acessar
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## Observações
- Se precisar de fallback SQLite para dev, exporte `DJANGO_USE_SQLITE=1`.
>>>>>>> f1c1fef (Atualizar README com instruções para SQLite e PostgreSQL; adicionar .gitignore)
