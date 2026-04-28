# 📊 Documentação do Banco de Dados - Sistema RH

## 🐳 Instalação e Configuração Docker + PostgreSQL

### Pré-requisitos

- **Docker Desktop** instalado
  - Download: https://www.docker.com/products/docker-desktop
  - Instale e reinicie o Windows

### ⚡ Paso 1: Iniciar PostgreSQL com Docker

Abra o **PowerShell** na pasta do projeto:

```powershell
cd c:\Users\nando\Downloads\Projeto_Python_RH-master

# Iniciar o container PostgreSQL
docker-compose up -d

# Verificar se está rodando
docker ps
```

**Esperado:**
```
CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS             PORTS
xxx            postgres:15-alpine  "docker-entrypoint..."  30 seconds ago  Up 28 seconds      0.0.0.0:5432->5432/tcp
```

---

### ⚡ Paso 2: Configurar Django para PostgreSQL

Edite o arquivo `rh_system/settings.py` e **substitua a seção DATABASES**:

```python
import os

# Verificar se está usando PostgreSQL
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
else:
    # SQLite (padrão)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

---

### ⚡ Paso 3: Definir Variáveis de Ambiente

**PowerShell:**

```powershell
$env:DJANGO_USE_POSTGRES="1"
$env:POSTGRES_DB="rh_system"
$env:POSTGRES_USER="rh_user"
$env:POSTGRES_PASSWORD="senha_segura_123"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
```

**Ou crie um arquivo `.env` na raiz do projeto:**

```
DJANGO_USE_POSTGRES=1
POSTGRES_DB=rh_system
POSTGRES_USER=rh_user
POSTGRES_PASSWORD=senha_segura_123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

### ⚡ Paso 4: Executar Migrações

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\activate

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
# Preencha com: username: admin, email: admin@example.com, password: admin123

# Iniciar servidor
python manage.py runserver
```

**Esperado:**
```
System check identified no issues (0 silenced).
April 08, 2026 - 10:30:00
Django version 6.0.3, using settings 'rh_system.settings'
Starting development server at http://127.0.0.1:8000/
```

---

### ⚡ Paso 5: Acessar a Aplicação

Abra no navegador:

- **Sistema RH:** http://127.0.0.1:8000
- **Admin Django:** http://127.0.0.1:8000/admin (use admin/admin123)

---

## 📋 Modelo Relacional (MER - Modelo Entidade-Relacionamento)

```
┌─────────────────────────────────┐
│         DEPARTAMENTO             │
├─────────────────────────────────┤
│ PK: id (INT)                    │
│ • nome (VARCHAR 100) - UNIQUE   │
│ • sigla (VARCHAR 10) - UNIQUE   │
└─────────────────────────────────┘
            │
            │ 1:N
            ▼
┌─────────────────────────────────┐         ┌──────────────────────────┐
│         FUNCIONARIO              │◄────────┤      FERIAS              │
├─────────────────────────────────┤         ├──────────────────────────┤
│ PK: id (INT)                    │ N       │ PK: id (INT)             │
│ • nome (VARCHAR 120)            │         │ • funcionario_id (FK)    │
│ • cpf (VARCHAR 14) - UNIQUE     │ 1       │ • data_inicio (DATE)     │
│ • cargo (VARCHAR 80)            │         │ • data_fim (DATE)        │
│ • salario (DECIMAL 12,2)        │         └──────────────────────────┘
│ • data_admissao (DATE)          │
│ • departamento_id (FK)          │
└─────────────────────────────────┘
```

### Relacionamentos

| Relação | Tipo | Descrição |
|---------|------|-----------|
| DEPARTAMENTO → FUNCIONARIO | 1:N | Um departamento tem múltiplos funcionários |
| FUNCIONARIO → FERIAS | 1:N | Um funcionário pode ter múltiplos períodos de férias |

### Cardinalidade

**DEPARTAMENTO (1) ─── (N) FUNCIONARIO**
- Um departamento obrigatoriamente existe
- Um funcionário pertence a exatamente um departamento
- Protection: Não permite deletar departamento com funcionários

**FUNCIONARIO (1) ─── (N) FERIAS**
- Um funcionário pode ter zero ou mais períodos de férias
- Um período de férias pertence a exatamente um funcionário
- Cascata: Deletar funcionário remove suas férias

---

## 💾 Modelo Físico (DDL - Data Definition Language)

### DDL PostgreSQL Gerado pelo Django

```sql
-- Tabela: DEPARTAMENTO
CREATE TABLE core_departamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    sigla VARCHAR(10) NOT NULL UNIQUE
);

CREATE INDEX idx_departamento_nome ON core_departamento(nome);
CREATE INDEX idx_departamento_sigla ON core_departamento(sigla);

-- Tabela: FUNCIONARIO
CREATE TABLE core_funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    cargo VARCHAR(80) NOT NULL,
    salario NUMERIC(12, 2) NOT NULL,
    data_admissao DATE NOT NULL,
    departamento_id INTEGER NOT NULL REFERENCES core_departamento(id) ON DELETE PROTECT
);

CREATE INDEX idx_funcionario_nome ON core_funcionario(nome);
CREATE INDEX idx_funcionario_cpf ON core_funcionario(cpf);
CREATE INDEX idx_funcionario_departamento ON core_funcionario(departamento_id);

-- Tabela: FERIAS
CREATE TABLE core_ferias (
    id SERIAL PRIMARY KEY,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    funcionario_id INTEGER NOT NULL REFERENCES core_funcionario(id) ON DELETE CASCADE
);

CREATE INDEX idx_ferias_funcionario ON core_ferias(funcionario_id);
CREATE INDEX idx_ferias_data_inicio ON core_ferias(data_inicio);
CREATE INDEX idx_ferias_data_fim ON core_ferias(data_fim);
```

---

## 📊 Estrutura de Dados Detalhada

### Tabela: DEPARTAMENTO

| Coluna | Tipo | Restrição | Descrição |
|--------|------|-----------|-----------|
| id | SERIAL | PK | Identificador único |
| nome | VARCHAR(100) | NOT NULL, UNIQUE | Nome do departamento |
| sigla | VARCHAR(10) | NOT NULL, UNIQUE | Sigla (ex: RH, TI, FIN) |

**Exemplo:**
```sql
INSERT INTO core_departamento (nome, sigla) VALUES 
  ('Recursos Humanos', 'RH'),
  ('Tecnologia da Informação', 'TI'),
  ('Finanças', 'FIN');
```

---

### Tabela: FUNCIONARIO

| Coluna | Tipo | Restrição | Descrição |
|--------|------|-----------|-----------|
| id | SERIAL | PK | Identificador único |
| nome | VARCHAR(120) | NOT NULL | Nome completo |
| cpf | VARCHAR(14) | NOT NULL, UNIQUE | CPF (formato: XXX.XXX.XXX-XX) |
| cargo | VARCHAR(80) | NOT NULL | Cargo/Função |
| salario | NUMERIC(12,2) | NOT NULL | Salário mensal (R$) |
| data_admissao | DATE | NOT NULL | Data de contratação |
| departamento_id | INTEGER | FK, NOT NULL | Referência ao departamento |

**Exemplo:**
```sql
INSERT INTO core_funcionario 
  (nome, cpf, cargo, salario, data_admissao, departamento_id) 
VALUES 
  ('João Silva', '123.456.789-00', 'Desenvolvedor Junior', 3500.00, '2023-01-15', 2),
  ('Maria Santos', '987.654.321-00', 'Analista RH', 4500.00, '2022-06-10', 1);
```

---

### Tabela: FERIAS

| Coluna | Tipo | Restrição | Descrição |
|--------|------|-----------|-----------|
| id | SERIAL | PK | Identificador único |
| data_inicio | DATE | NOT NULL | Primeiro dia de férias |
| data_fim | DATE | NOT NULL | Último dia de férias |
| funcionario_id | INTEGER | FK, NOT NULL | Referência ao funcionário |

**Validações:**
- `data_fim > data_inicio` (data fim deve ser após data início)
- `(data_fim - data_inicio) ≤ 30 dias` (máximo 30 dias)

**Exemplo:**
```sql
INSERT INTO core_ferias (data_inicio, data_fim, funcionario_id)
VALUES 
  ('2026-07-01', '2026-07-15', 1),
  ('2026-08-01', '2026-08-20', 2);
```

---

## 🔑 Chaves e Índices

### Chaves Primárias
- `core_departamento.id` - SERIAL (auto-increment)
- `core_funcionario.id` - SERIAL (auto-increment)
- `core_ferias.id` - SERIAL (auto-increment)

### Chaves Estrangeiras
- `core_funcionario.departamento_id` → `core_departamento.id` (ON DELETE PROTECT)
- `core_ferias.funcionario_id` → `core_funcionario.id` (ON DELETE CASCADE)

### Índices de Performance
```sql
-- Busca rápida por nome
CREATE INDEX idx_funcionario_nome ON core_funcionario(nome);

-- Validação CPF único
CREATE INDEX idx_funcionario_cpf ON core_funcionario(cpf);

-- Filtro por departamento
CREATE INDEX idx_funcionario_departamento ON core_funcionario(departamento_id);

-- Filtro de férias
CREATE INDEX idx_ferias_funcionario ON core_ferias(funcionario_id);
CREATE INDEX idx_ferias_data_inicio ON core_ferias(data_inicio);
CREATE INDEX idx_ferias_data_fim ON core_ferias(data_fim);
```

---

## 📈 Consultas SQL Comuns

### Listar todos os funcionários por departamento

```sql
SELECT 
    d.nome AS departamento,
    f.nome AS funcionario,
    f.cargo,
    f.salario,
    f.data_admissao
FROM core_funcionario f
JOIN core_departamento d ON f.departamento_id = d.id
ORDER BY d.nome, f.nome;
```

---

### Funcionários em férias hoje

```sql
SELECT 
    f.nome,
    f.cargo,
    d.nome AS departamento,
    fc.data_inicio,
    fc.data_fim
FROM core_ferias fc
JOIN core_funcionario f ON fc.funcionario_id = f.id
JOIN core_departamento d ON f.departamento_id = d.id
WHERE fc.data_inicio <= CURRENT_DATE AND fc.data_fim >= CURRENT_DATE;
```

---

### Folha de pagamento por departamento

```sql
SELECT 
    d.nome AS departamento,
    COUNT(f.id) AS total_funcionarios,
    SUM(f.salario) AS total_folha,
    AVG(f.salario) AS salario_medio
FROM core_departamento d
LEFT JOIN core_funcionario f ON d.id = f.departamento_id
GROUP BY d.nome
ORDER BY total_folha DESC;
```

---

### Tempo de empresa

```sql
SELECT 
    f.nome,
    f.data_admissao,
    CURRENT_DATE - f.data_admissao AS dias_na_empresa,
    ROUND((CURRENT_DATE - f.data_admissao)::numeric / 365.25, 1) AS anos_na_empresa
FROM core_funcionario f
ORDER BY f.data_admissao;
```

---

## 🛠️ Gerenciar PostgreSQL com Docker

### Listar containers rodando

```powershell
docker ps
```

---

### Acessar o PostgreSQL pelo CLI

```powershell
# Conectar ao banco
docker exec -it postgres_rh psql -U rh_user -d rh_system

# Dentro do psql, você pode:
\dt                    # Listar todas as tabelas
\d core_funcionario   # Descrição da tabela
SELECT * FROM core_departamento;  # Consultar dados
\q                    # Sair
```

---

### Fazer backup do banco

```powershell
# Fazer backup
docker exec postgres_rh pg_dump -U rh_user -d rh_system > backup_rh.sql

# Restaurar backup
docker exec -i postgres_rh psql -U rh_user -d rh_system < backup_rh.sql
```

---

### Parar e remover container

```powershell
# Parar container
docker-compose down

# Remover dados (cuidado!)
docker-compose down -v
```

---

## 📋 Status do Sistema

✅ **Docker Compose:** Configurado  
✅ **PostgreSQL:** 15-Alpine  
✅ **Conexão Django:** Configurada  
✅ **Variáveis de Ambiente:** .env.postgres  

**Próximo passo:** Instale Docker Desktop e execute `docker-compose up -d`

---

## 📞 Troubleshooting

### ❌ Erro: "docker: command not found"
- Instale Docker Desktop: https://www.docker.com/products/docker-desktop

### ❌ Erro: "could not connect to server"
- Verifique: `docker ps`
- Reinicie: `docker-compose restart`

### ❌ Erro: "FATAL: role 'rh_user' does not exist"
- Recrie o container: `docker-compose down -v && docker-compose up -d`

---

**Última atualização:** Abril 2026
