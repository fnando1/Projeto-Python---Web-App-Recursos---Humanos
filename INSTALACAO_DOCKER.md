# 🐳 Guia Detalhado: Instalação Docker + PostgreSQL

## 📋 Verificação de Pré-requisitos

### Windows 10/11 (Verificar versão)

```powershell
Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber
```

**Para Docker, você precisa:**
- Windows 10 Pro/Enterprise/Education (Build 2004+)
- OU Windows 11
- 4GB RAM mínimo
- Virtualization habilitada (BIOS)

---

## 🚀 Passo 1: Instalar Docker Desktop

### Download

Vá para: https://www.docker.com/products/docker-desktop

Clique em **Docker Desktop for Windows**

### Instalar

1. Execute o instalador `.exe`
2. Marque:
   - ✅ Install required Windows components for WSL 2
   - ✅ Add Docker to PATH
3. Clique **OK** e aguarde
4. **Reinicie o computador**

### Verificar Instalação

Abra **PowerShell** e execute:

```powershell
docker --version
# Esperado: Docker version 24.0.0 (ou superior)

docker run hello-world
# Esperado: "Hello from Docker!" aparecer
```

---

## 📦 Passo 2: Iniciar PostgreSQL com Docker

### Opção A: Usando docker-compose (Recomendado)

**Vá até a pasta do projeto:**

```powershell
cd c:\Users\nando\Downloads\Projeto_Python_RH-master
```

**Execute:**

```powershell
docker-compose up -d
```

**Aguarde alguns segundos e verifique:**

```powershell
docker ps
```

**Você deve ver:**
```
CONTAINER ID   IMAGE               STATUS              PORTS
abc123def456   postgres:15-alpine  Up 10 seconds       0.0.0.0:5432->5432/tcp
```

---

### Opção B: Comando Docker Manual

Se não tiver `docker-compose.yml`:

```powershell
docker run --name postgres_rh `
  -e POSTGRES_DB=rh_system `
  -e POSTGRES_USER=rh_user `
  -e POSTGRES_PASSWORD=senha_segura_123 `
  -p 5432:5432 `
  -d `
  postgres:15-alpine
```

---

## 🔗 Passo 3: Testar Conexão PostgreSQL

### Via Docker CLI

```powershell
docker exec -it postgres_rh psql -U rh_user -d rh_system
```

**Dentro do psql:**

```sql
\dt                    -- Listar tabelas (vazio no início)
SELECT version();      -- Ver versão do PostgreSQL
\q                     -- Sair
```

---

## ⚙️ Passo 4: Configurar Django

### Editar `rh_system/settings.py`

Abra com um editor de texto (VS Code, Notepad++, etc):

**Procure por esta seção (linha ~60):**

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

**Verifique se existe este código após (linhas ~65-78):**

```python
if os.environ.get("DJANGO_USE_POSTGRES", "0") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "rh_system"),
            "USER": os.environ.get("POSTGRES_USER", "rh_user"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "senha_segura_123"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
```

**Se não existir, adicione!**

---

## 🔐 Passo 5: Definir Variáveis de Ambiente

### Opção A: PowerShell (por sessão)

```powershell
$env:DJANGO_USE_POSTGRES="1"
$env:POSTGRES_DB="rh_system"
$env:POSTGRES_USER="rh_user"
$env:POSTGRES_PASSWORD="senha_segura_123"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"

# Verificar
echo $env:DJANGO_USE_POSTGRES
# Esperado: 1
```

### Opção B: Arquivo .env (Permanente)

Na raiz do projeto, crie arquivo `.env`:

```
DJANGO_USE_POSTGRES=1
POSTGRES_DB=rh_system
POSTGRES_USER=rh_user
POSTGRES_PASSWORD=senha_segura_123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Para usar o arquivo `.env`, instale python-dotenv:

```powershell
pip install python-dotenv
```

Adicione ao topo de `settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega .env
```

### Opção C: Variáveis de Sistema (Windows)

1. Abra **Configurações** > **Sistema** > **Sobre**
2. Clique em **Variáveis de ambiente**
3. Clique em **Novo** e adicione:
   - Nome: `DJANGO_USE_POSTGRES`
   - Valor: `1`
4. Repita para as outras variáveis
5. **Reinicie o PowerShell**

---

## 📦 Passo 6: Executar Migrações

```powershell
# Ativar venv
.\.venv\Scripts\activate

# Executar migrate
python manage.py migrate
```

**Esperado:**

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions

Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying core.0001_initial... OK
  ...
  OK
```

---

## 👤 Passo 7: Criar Superusuário

```powershell
python manage.py createsuperuser
```

**Preencha com:**

```
Username: admin
Email address: admin@example.com
Password: admin123
Password (again): admin123
```

---

## 🚀 Passo 8: Iniciar Servidor

```powershell
python manage.py runserver
```

**Esperado:**

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🌐 Acessar Sistema

### Abra navegador:

- **Sistema:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin
  - Usuário: `admin`
  - Senha: `admin123`

---

## 🐛 Troubleshooting

### ❌ Erro: "Docker daemon not running"

**Solução:**
1. Abra **Docker Desktop** (procure no menu Start)
2. Aguarde inicializar (pode levar 1-2 minutos)
3. Tente novamente

---

### ❌ Erro: "Port 5432 already in use"

**Solução 1 - Parar container antigo:**

```powershell
docker stop postgres_rh
docker rm postgres_rh
docker-compose up -d
```

**Solução 2 - Usar porta diferente:**

Edite `docker-compose.yml`:

```yaml
ports:
  - "5433:5432"  # Alterado de 5432 para 5433
```

Configure variável:
```powershell
$env:POSTGRES_PORT="5433"
```

---

### ❌ Erro: "could not connect to server"

**Verificar:**

```powershell
docker ps
# Container running?

docker logs postgres_rh
# Ver logs de erro
```

**Soluções:**

```powershell
# Reiniciar container
docker restart postgres_rh

# Ou recriá-lo
docker-compose down
docker-compose up -d
```

---

### ❌ Erro: "FATAL: role 'rh_user' does not exist"

**Solução:**

```powershell
# Parar e remover
docker-compose down -v

# Recrear (sem volumes antigos)
docker-compose up -d

# Wait 10 seconds, then migrate
python manage.py migrate
```

---

### ❌ Erro: "psycopg2.OperationalError: FATAL: database 'rh_system' does not exist"

**Verificar:**

```powershell
docker exec postgres_rh psql -U postgres -l
```

**Se não existir, criar:**

```powershell
docker exec postgres_rh psql -U postgres -c "CREATE DATABASE rh_system;"
```

---

### ❌ "ModuleNotFoundError: No module named 'psycopg2'"

**Solução:**

```powershell
pip install psycopg2-binary
```

---

### ❌ Variáveis de ambiente não carregam

**Solução:**

Use arquivo `.env` com `python-dotenv`:

```powershell
pip install python-dotenv
```

Edite `settings.py`:

```python
from pathlib import Path
from dotenv import load_dotenv
import os

# Carregar .env
load_dotenv(Path(__file__).parent.parent / '.env')

BASE_DIR = Path(__file__).resolve().parent.parent
```

---

## 🛑 Parar Sistema

```powershell
# Parar Django (no PowerShell onde rodava)
CTRL + C

# Parar PostgreSQL (opcional - mantém dados)
docker-compose down

# Parar E remover dados (CUIDADO!)
docker-compose down -v
```

---

## 💾 Gerenciar Banco de Dados

### Fazer Backup

```powershell
docker exec postgres_rh pg_dump -U rh_user -d rh_system > backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').sql
```

### Listar Backups

```powershell
Get-ChildItem backup_*.sql
```

### Restaurar Backup

```powershell
docker exec -i postgres_rh psql -U rh_user -d rh_system < backup_2026-04-08_10-30-00.sql
```

---

## 📊 Monitorar PostgreSQL

### Ver Logs

```powershell
docker logs -f postgres_rh
```

### Usar pgAdmin (Interface Web)

Opcionalmente, adicione ao `docker-compose.yml`:

```yaml
pgadmin:
  image: dpage/pgadmin4
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@pgadmin.com
    PGADMIN_DEFAULT_PASSWORD: admin
  ports:
    - "5050:80"
  depends_on:
    - postgres
```

Acesse: http://127.0.0.1:5050

---

## ✅ Checklist Final

- [ ] Docker Desktop instalado
- [ ] PostgreSQL rodando (`docker ps`)
- [ ] Variáveis de ambiente definidas
- [ ] `settings.py` configurado para PostgreSQL
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Servidor rodando em http://127.0.0.1:8000
- [ ] Admin acessível em http://127.0.0.1:8000/admin

---

**Documentação criada em:** Abril 2026  
**Última atualização:** Abril 2026
