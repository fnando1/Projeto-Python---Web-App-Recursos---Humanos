# ⚡ Quick Start - PostgreSQL + Docker (em 5 minutos)

## 📋 Pré-requisitos

- ✅ Docker Desktop instalado: https://www.docker.com/products/docker-desktop
- ✅ Projeto clonado/baixado
- ✅ Python 3.8+ com venv ativado

---

## 🚀 Passo 1: Iniciar PostgreSQL

```powershell
cd c:\Users\nando\Downloads\Projeto_Python_RH-master

docker-compose up -d
```

**Verificar se subiu:**
```powershell
docker ps
# Deve ver: postgres_rh rodando
```

---

## 🚀 Passo 2: Ativar Ambiente Virtual

```powershell
.\.venv\Scripts\activate
# Deve aparecer (venv) no início da linha
```

---

## 🚀 Passo 3: Configurar Variáveis de Ambiente

```powershell
$env:DJANGO_USE_POSTGRES="1"
$env:POSTGRES_DB="rh_system"
$env:POSTGRES_USER="rh_user"
$env:POSTGRES_PASSWORD="senha_segura_123"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
```

---

## 🚀 Passo 4: Executar Migrações

```powershell
python manage.py migrate
```

**Esperado:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  ...
  OK
```

---

## 🚀 Passo 5: Criar Superusuário (Admin)

```powershell
python manage.py createsuperuser
```

**Preencha com:**
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

---

## 🚀 Passo 6: Iniciar o Servidor

```powershell
python manage.py runserver
```

**Esperado:**
```
Starting development server at http://127.0.0.1:8000/
Press CTRL+C to quit.
```

---

## 🌐 Acessar a Aplicação

Abra no navegador:

### 📍 Sistema RH
http://127.0.0.1:8000

### 📍 Dashboard Admin
http://127.0.0.1:8000/admin
- Usuário: `admin`
- Senha: `admin123`

---

## 📊 Ver Dados no PostgreSQL

```powershell
# Em outro PowerShell, conectar ao banco
docker exec -it postgres_rh psql -U rh_user -d rh_system

# Dentro do psql:
SELECT * FROM core_departamento;
SELECT * FROM core_funcionario;
SELECT * FROM core_ferias;

# Sair
\q
```

---

## 🛑 Parar o Sistema

```powershell
# Parar o servidor Django
CTRL + C (no PowerShell onde rodava o servidor)

# Parar PostgreSQL
docker-compose down
```

---

## 📚 Documentação Completa

- **Banco de Dados:** [BANCO_DE_DADOS.md](BANCO_DE_DADOS.md)
- **Diagramas:** [DIAGRAMA_BANCO.md](DIAGRAMA_BANCO.md)
- **README:** [README.md](README.md)

---

## ❓ Problemas Comuns

### ❌ "docker: command not found"
→ Instale Docker Desktop

### ❌ "psycopg2.OperationalError: could not connect"
→ Verifique: `docker ps` (container rodando?)

### ❌ "FATAL: role 'rh_user' does not exist"
→ Recrie: `docker-compose down -v && docker-compose up -d`

### ❌ Variáveis de ambiente não persistem
→ Crie arquivo `.env` na raiz do projeto (ver .env.postgres)

---

**Pronto! Sistema rodando com PostgreSQL! 🎉**
