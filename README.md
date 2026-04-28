# 🎯 Sistema RH - Django

Um sistema completo de Recursos Humanos desenvolvido com Django, PostgreSQL/SQLite e Bootstrap 5. Gerencie funcionários, departamentos e período de férias com uma interface moderna e responsiva.

## ✨ Funcionalidades

### 👥 Gestão de Funcionários
- ✅ CRUD completo de funcionários
- ✅ Cadastro com CPF (validado), cargo, salário e data de admissão
- ✅ Filtro por departamento e busca por nome
- ✅ Detalhes com informações de departamento
- ✅ Exclusão com confirmação

### 🏢 Departamentos
- ✅ Cadastro de departamentos com siglas
- ✅ Associação obrigatória com funcionários
- ✅ Proteção contra exclusão (se tiver funcionários)

### 🏖️ Gestão de Férias
- ✅ Registro de períodos de férias
- ✅ Validação de datas (máx. 30 dias)
- ✅ Rastreamento de status (Planejadas/Em Andamento/Finalizada)
- ✅ Visualização por funcionário
- ✅ Dashboard com alertas de funcionários em férias

### 📊 Dashboard RH
- ✅ Total de funcionários
- ✅ Gasto com folha de pagamento
- ✅ Número de departamentos
- ✅ Funcionários em férias hoje
- ✅ Previsão de férias próximas (30 dias)
- ✅ Lista rápida de funcionários

### 🎨 Interface
- ✅ Bootstrap 5 responsivo
- ✅ Navbar com navegação
- ✅ Sidebar com menu
- ✅ Tabelas interativas
- ✅ Alertas e notificações
- ✅ Design mobile-friendly
- ✅ **Sistema de Temas Claro/Escuro** 🌙☀️

### 🔐 Admin Django
- ✅ Painel administrativo (http://localhost:8000/admin)
- ✅ Visualização de métricas formatadas
- ✅ Filtros por departamento e período

## 🗄️ Modelo de Dados

```
DEPARTAMENTO (1) ──── (N) FUNCIONARIO ──── (N) FERIAS
    ├─ id (PK)              ├─ id (PK)          ├─ id (PK)
    ├─ nome (UK)            ├─ nome             ├─ funcionario_id (FK)
    └─ sigla (UK)           ├─ cpf (UK)         ├─ data_inicio
                            ├─ cargo            └─ data_fim
                            ├─ salario
                            ├─ data_admissao
                            └─ departamento_id (FK)
```

### Validações
- **CPF:** Formato XXX.XXX.XXX-XX, validação de dígitos
- **Salário:** Apenas valores positivos
- **Data Admissão:** Não pode ser data futura
- **Férias:** Período máximo 30 dias, fim > início


## 🧽 Limpeza do Projeto (Atualizado - Abril 2026)

Foram removidos arquivos desnecessários para otimizar o projeto:

- ✅ **Removido:** `core/tests.py` - Arquivo vazio sem testes implementados
- ✅ **Removido:** `data.json` - Fixture não utilizada

A estrutura agora está mais limpa e mantém apenas os arquivos essenciais para o funcionamento do sistema.

---

## 🐳 PostgreSQL com Docker (Novo!)

Arquivos adicionados para facilitar configuração com PostgreSQL:

- 📄 **QUICKSTART_POSTGRES.md** - Guia rápido em 5 minutos
- 📄 **BANCO_DE_DADOS.md** - Documentação completa do banco
- 📄 **DIAGRAMA_BANCO.md** - Modelos relacional e físico
- 📦 **docker-compose.yml** - Configuração Docker
- 🔧 **setup-docker.ps1** - Script de setup automático
- .env.postgres - Variáveis de ambiente

**Start rápido:**
```powershell
docker-compose up -d  # Inicia PostgreSQL
python manage.py migrate  # Executa migrações
python manage.py runserver  # Roda sistema
---

## 🎨 Sistema de Temas

O sistema possui **tema claro e escuro** com alternância automática:

### 🌞 Tema Claro (Padrão)
- Fundo azul claro gradiente (#f5f7fa → #c3cfe2)
- Cards brancos (#ffffff)
- **Sidebar azul claro com texto preto**
- Design moderno e profissional

### 🌙 Tema Dark
- Fundo escuro elegante (#0f0f23 → #1a1a2e)
- Cards azul muito escuro (#1a1a2e)
- **Sidebar navy escuro com texto claro**
- Acentos em indigo (#6366f1)
- Design noturno confortável para os olhos

### 🔄 Como Alternar
- **Na Dashboard**: Botão destacado "Tema Claro/Dark" na página principal
- **Desktop**: Botão "Tema Claro/Dark" na sidebar ou botão flutuante no canto inferior direito
- **Mobile**: Botão "Tema" no menu hambúrguer ou botão flutuante
- **Botão Flutuante**: Sempre visível no canto inferior direito da tela
- **Persistência**: Preferência salva automaticamente no navegador

### ✨ Melhorias Visuais (Abril 2026)
- ✅ **Animações suaves**: Fade-in, slide-in e efeitos hover em todas as páginas
- ✅ **Gradientes modernos**: Botões com efeitos e sombras dinâmicas
- ✅ **Responsividade total**: Desktop, tablet e mobile otimizados
- ✅ **Tema Dark Profissional**: Paleta escura elegante com acentos indigo
- ✅ **Sidebar Colorida**: Azul claro (tema claro) e navy (tema dark)
- ✅ **Três Botões de Tema**: Dashboard, sidebar, botão flutuante
- ✅ **Efeitos visuais**: Cards com hover, transições suaves, animações

📄 **Documentação completa**: [TEMA_SISTEMA.md](TEMA_SISTEMA.md)

---

## 📋 Requisitos

- Python 3.8+
- Django 6.0+
- PostgreSQL 12+ (opcional) ou SQLite (padrão)
- pip/virtualenv
- Git

## 🚀 Instalação

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/Projeto_Python_RH.git
cd Projeto_Python_RH
```

---

## 🪟 INSTALAÇÃO NO WINDOWS

### 2️⃣ Criar ambiente virtual

Abra o **PowerShell** ou **Prompt de Comando** na pasta do projeto:

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Deve aparecer (venv) no prompt
```

### 3️⃣ Instalar dependências

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configurar banco de dados

#### SQLite (Recomendado para desenvolvimento - Padrão)

```powershell
# Executar migrações
python manage.py migrate

# Criar superusuário (admin)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Acesse: http://127.0.0.1:8000
# Admin: http://127.0.0.1:8000/admin
```

#### PostgreSQL (Para produção)

**1. Instale PostgreSQL:**
- Baixe em: https://www.postgresql.org/download/windows/
- Durante instalação, anote a senha do usuário `postgres`

**2. Crie o banco de dados (abra pgAdmin ou psql):**

```sql
CREATE DATABASE rh_system;
CREATE USER rh_user WITH PASSWORD 'sua_senha';
ALTER ROLE rh_user SET client_encoding TO 'utf8';
ALTER ROLE rh_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE rh_user SET default_transaction_deferrable TO on;
ALTER ROLE rh_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE rh_system TO rh_user;
```

**3. Configure em `rh_system/settings.py`:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rh_system',
        'USER': 'rh_user',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**4. Execute no PowerShell:**

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🐧 INSTALAÇÃO NO UBUNTU/LINUX

### 2️⃣ Criar ambiente virtual

```bash
# Atualizar pip
sudo apt update
sudo apt install python3-pip python3-venv -y

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Deve aparecer (venv) no prompt
```

### 3️⃣ Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configurar banco de dados

#### SQLite (Recomendado para desenvolvimento - Padrão)

```bash
# Executar migrações
python manage.py migrate

# Criar superusuário (admin)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Acesse: http://127.0.0.1:8000
# Admin: http://127.0.0.1:8000/admin
```

#### PostgreSQL (Para produção)

**1. Instale PostgreSQL:**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y  # Necessário para psycopg2
```

**2. Crie o banco de dados:**

```bash
# Entre como usuário postgres
sudo -u postgres psql

# No prompt do PostgreSQL, execute:
CREATE DATABASE rh_system;
CREATE USER rh_user WITH PASSWORD 'sua_senha';
ALTER ROLE rh_user SET client_encoding TO 'utf8';
ALTER ROLE rh_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE rh_user SET default_transaction_deferrable TO on;
ALTER ROLE rh_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE rh_system TO rh_user;

# Digite \q para sair
```

**3. Configure em `rh_system/settings.py`:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rh_system',
        'USER': 'rh_user',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**4. Execute os comandos:**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

### 5️⃣ Acessar a aplicação

Abra seu navegador e acesse:

- **Sistema RH:** http://127.0.0.1:8000
- **Painel Admin:** http://127.0.0.1:8000/admin (use as credenciais do superusuário)

## 📍 URLs Disponíveis

### Frontend
| URL | Descrição |
|-----|-----------|
| `/` | Dashboard RH |
| `/funcionarios/` | Lista de funcionários |
| `/funcionarios/novo/` | Criar funcionário |
| `/funcionarios/<id>/` | Detalhes do funcionário |
| `/funcionarios/<id>/editar/` | Editar funcionário |
| `/funcionarios/<id>/excluir/` | Excluir funcionário |
| `/ferias/` | Lista de férias |
| `/ferias/novo/` | Registrar férias |
| `/ferias/<id>/` | Detalhes das férias |
| `/ferias/<id>/editar/` | Editar férias |
| `/ferias/<id>/excluir/` | Excluir férias |
| `/departamentos/novo/` | Criar departamento |

### Admin
| URL | Descrição |
|-----|-----------|
| `/admin/` | Painel administrativo Django |

## 💻 Como Usar

### Criar Funcionário
1. Navegue para "Funcionários" no menu
2. Clique em "+ Novo Funcionário"
3. Preencha os dados (CPF format: XXX.XXX.XXX-XX)
4. Selecione um departamento
5. Clique em "Salvar"

### Registrar Férias
1. Vá para "Férias" no menu
2. Clique em "+ Registrar Férias"
3. Selecione o funcionário
4. Informar datas (máx 30 dias)
5. Submeta o formulário

### Filtrar Funcionários
1. Na página de funcionários
2. Use a barra de busca por nome
3. Selecione um departamento no dropdown
4. Clique em "Filtrar"

### Visualizar Dashboard
1. Acesse a página inicial (/)
2. Veja métricas gerais
3. Confira funcionários em férias
4. Visualize previsão de férias próximas

## 🔧 Estrutura do Projeto

```
Projeto_Python_RH/
├── core/                          # Aplicação principal Django
│   ├── migrations/                # Migrações do banco
│   ├── templates/core/            # Templates HTML
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── funcionario_list.html
│   │   ├── funcionario_form.html
│   │   ├── funcionario_detail.html
│   │   ├── ferias_list.html
│   │   ├── ferias_form.html
│   │   ├── ferias_detail.html
│   │   ├── ferias_confirm_delete.html
│   │   ├── departamento_form.html
│   │   ├── er_diagram.html
│   │   └── home.html
│   ├── admin.py                   # Configuração do admin
│   ├── forms.py                   # Formulários Django
│   ├── models.py                  # Modelos de dados
│   ├── views.py                   # Views/Controladores
│   ├── urls.py                    # Rotas
│   ├── apps.py                    # Config da aplicação
│   └── __init__.py
├── rh_system/                     # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
├── manage.py                      # CLI Django
├── requirements.txt               # Dependências Python
├── db.sqlite3                     # Banco SQLite (dev)
├── README.md                      # Este arquivo
└── .gitignore                     # Git ignore
```

## 📦 Dependências

```
Django==6.0.3
django-crispy-forms==2.6
crispy-bootstrap5==2026.3
psycopg2-binary==2.9.11 (para PostgreSQL)
```

Ver `requirements.txt` para lista completa.

## 📝 Migrações

Criar nova migração após alterar modelos:

```bash
# Windows
python manage.py makemigrations
python manage.py migrate

# Ubuntu/Linux
python manage.py makemigrations
python manage.py migrate
```

## 🐛 Resolução de Problemas

### ❌ Erro: "django.db.utils.OperationalError: no such table"

**Solução:**
```bash
python manage.py migrate
```

### ❌ Erro: "ModuleNotFoundError: No module named 'django'"

**Windows:**
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

**Ubuntu/Linux:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ Erro: "psycopg2.OperationalError: FATAL: database does not exist"

**Solução:**
- Crie o banco: `CREATE DATABASE rh_system;`
- Configure as credenciais em `rh_system/settings.py`
- Execute: `python manage.py migrate`

### ❌ Erro: "ValueError: invalid literal for int()"

**Solução:**
- Verifique se o banco foi criado corretamente
- Execute: `python manage.py migrate`

### ❌ Superusuário não funciona

**Solução:**
```bash
python manage.py createsuperuser
```

### ❌ Porta 8000 já está em uso

**Windows/Ubuntu:**
```bash
python manage.py runserver 8001  # ou outra porta
```

---

## 📄 Licença

MIT License - Veja LICENSE para detalhes

## 👨‍💻 Autor

Sistema RH desenvolvido como projeto educacional em Django.

## 🤝 Contribuições

Contributions are welcome! Por favor abra uma issue ou pull request.

---

**Status:** ✅ Ativo e Funcional  
**Última atualização:** Abril 2026  
**Versão:** 1.1 (Com limpeza de arquivos desnecessários)  
**Compatibilidade:** Windows 10+, Ubuntu 20.04+, macOS
#   P r o j e t o - P y t h o n - - - W e b - A p p - R e c u r s o s - - - H u m a n o s  
 