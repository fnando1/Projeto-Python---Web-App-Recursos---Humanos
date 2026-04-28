# 📊 Diagrama Visual do Banco de Dados

## Modelo Relacional - MER (Visual)

```
╔═════════════════════════════════╗
║       DEPARTAMENTO              ║
╠═════════════════════════════════╣
║ PK  id: INT                     ║
║ UQ  nome: VARCHAR(100)          ║
║ UQ  sigla: VARCHAR(10)          ║
╚═════════════════════════════════╝
              │
              │ 1:N (1 departamento → N funcionários)
              │ PROTECT: Impossível deletar dept com funcionários
              │
              ▼
╔═════════════════════════════════╗         ╔═════════════════════════════════╗
║       FUNCIONARIO               ║◄────────║          FERIAS                 ║
╠═════════════════════════════════╣  1:N    ╠═════════════════════════════════╣
║ PK  id: INT                     ║ (1 emp  ║ PK  id: INT                     ║
║ UQ  cpf: VARCHAR(14)            ║  → N    ║ FK  funcionario_id: INT         ║
║     nome: VARCHAR(120)          ║  férias)║     data_inicio: DATE           ║
║     cargo: VARCHAR(80)          ║         ║     data_fim: DATE              ║
║     salario: DECIMAL(12,2)      ║         ║     (máx 30 dias)               ║
║     data_admissao: DATE         ║         ║ CASCADE: Deleta férias          ║
║ FK  departamento_id: INT        ║         ║         quando emp deletado     ║
╚═════════════════════════════════╝         ╚═════════════════════════════════╝
```

---

## Exemplo de Dados

### DEPARTAMENTO
```
┌────┬──────────────────┬────────┐
│ id │      nome        │ sigla  │
├────┼──────────────────┼────────┤
│ 1  │ Recursos Humanos │   RH   │
│ 2  │ Tecnologia       │   TI   │
│ 3  │ Finanças         │  FIN   │
└────┴──────────────────┴────────┘
```

### FUNCIONARIO
```
┌────┬───────────────────┬─────────────────┬──────────────────────┬──────────┬────────────────┬────────────────┐
│ id │      nome         │       cpf       │       cargo          │ salario  │ data_admissao  │ dept_id │
├────┼───────────────────┼─────────────────┼──────────────────────┼──────────┼────────────────┼────────────────┤
│ 1  │ João Silva        │ 123.456.789-00  │ Dev Junior           │ 3500.00  │ 2023-01-15     │ 2      │
│ 2  │ Maria Santos      │ 987.654.321-00  │ Analista RH          │ 4500.00  │ 2022-06-10     │ 1      │
│ 3  │ Carlos Oliveira   │ 456.789.123-00  │ Gerente Financeiro   │ 6000.00  │ 2021-03-20     │ 3      │
│ 4  │ Ana Costa         │ 789.123.456-00  │ Dev Senior           │ 5500.00  │ 2020-11-05     │ 2      │
└────┴───────────────────┴─────────────────┴──────────────────────┴──────────┴────────────────┴────────────────┘
```

### FERIAS
```
┌────┬──────────────┬──────────────┬────────────────┐
│ id │ data_inicio  │  data_fim    │ funcionario_id │
├────┼──────────────┼──────────────┼────────────────┤
│ 1  │ 2026-07-01   │ 2026-07-15   │ 1              │
│ 2  │ 2026-08-01   │ 2026-08-20   │ 2              │
│ 3  │ 2026-06-15   │ 2026-07-02   │ 3              │
│ 4  │ 2026-09-10   │ 2026-09-25   │ 4              │
└────┴──────────────┴──────────────┴────────────────┘
```

---

## Relacionamentos Visuais

### Consulta: Funcionários por Departamento

```
RH (Dept 1) ──┐
              ├─ Maria Santos (Analista RH) ─ Férias: 2026-08-01 a 2026-08-20
              └─ ...

TI (Dept 2) ──┐
              ├─ João Silva (Dev Junior) ─ Férias: 2026-07-01 a 2026-07-15
              ├─ Ana Costa (Dev Senior) ─ Férias: 2026-09-10 a 2026-09-25
              └─ ...

FIN (Dept 3) ──┐
               ├─ Carlos Oliveira (Gerente) ─ Férias: 2026-06-15 a 2026-07-02
               └─ ...
```

---

## Restrições de Integridade

### 1️⃣ Chave Primária (PK)
- `DEPARTAMENTO.id` → Cada departamento tem ID único
- `FUNCIONARIO.id` → Cada funcionário tem ID único
- `FERIAS.id` → Cada período de férias tem ID único

### 2️⃣ Chave Única (UQ)
- `DEPARTAMENTO.nome` → Nomes de departamentos não se repetem
- `DEPARTAMENTO.sigla` → Siglas não se repetem
- `FUNCIONARIO.cpf` → CPFs não se repetem (Validação: 11 dígitos)

### 3️⃣ Chave Estrangeira (FK)
- `FUNCIONARIO.departamento_id` → Refs `DEPARTAMENTO.id`
  - **ON DELETE PROTECT:** Impossível deletar departamento se tem funcionários
  - **Exemplo:** `DELETE FROM DEPARTAMENTO WHERE id=1` → Erro!

- `FERIAS.funcionario_id` → Refs `FUNCIONARIO.id`
  - **ON DELETE CASCADE:** Deleta férias quando funcionário é deletado
  - **Exemplo:** `DELETE FROM FUNCIONARIO WHERE id=1` → Deleta férias automático

### 4️⃣ NOT NULL
- Todas as colunas sem padrão precisam de valor

### 5️⃣ CHECK (Validações de Negócio)
```sql
-- Salário não pode ser negativo
ALTER TABLE core_funcionario ADD CHECK (salario >= 0);

-- Data de término deve ser após data de início
ALTER TABLE core_ferias ADD CHECK (data_fim > data_inicio);

-- Férias não podem ultrapassar 30 dias
ALTER TABLE core_ferias ADD CHECK ((data_fim - data_inicio) <= 30);
```

---

## Índices para Performance

```
DEPARTAMENTO
├─ idx_departamento_nome → Busca por nome
└─ idx_departamento_sigla → Busca por sigla

FUNCIONARIO
├─ idx_funcionario_nome → Busca por nome (filtros)
├─ idx_funcionario_cpf → Lookup único de CPF
└─ idx_funcionario_departamento → Filtros por dept

FERIAS
├─ idx_ferias_funcionario → Listar férias do funcionário
├─ idx_ferias_data_inicio → Buscar férias por data
└─ idx_ferias_data_fim → Filtros de período
```

---

## Transações e ACID

### Atomicidade (A)
```sql
BEGIN;
INSERT INTO core_funcionario (nome, cpf, ...) VALUES (...);
INSERT INTO core_ferias (data_inicio, ...) VALUES (...);
COMMIT;  -- Tudo ou nada
```

### Consistência (C)
- Restrições FK garantem que todo funcionário tem dept válido
- Checks garantem salário > 0, férias ≤ 30 dias

### Isolamento (I)
- Transações simultâneas não interferem uma na outra

### Durabilidade (D)
- Dados persistidos no disco (WAL - Write-Ahead Logging)

---

## Vistas Úteis (Views)

### View: Funcionários com Informações Completas

```sql
CREATE VIEW vw_funcionario_completo AS
SELECT
    f.id,
    f.nome,
    f.cpf,
    f.cargo,
    f.salario,
    f.data_admissao,
    d.nome AS departamento,
    d.sigla AS sigla_departamento,
    CURRENT_DATE - f.data_admissao AS dias_na_empresa,
    ROUND((CURRENT_DATE - f.data_admissao)::numeric / 365.25, 1) AS anos_na_empresa
FROM core_funcionario f
LEFT JOIN core_departamento d ON f.departamento_id = d.id;

-- Uso:
SELECT * FROM vw_funcionario_completo;
```

### View: Férias Próximas

```sql
CREATE VIEW vw_ferias_proximas AS
SELECT
    f.id,
    func.nome AS funcionario,
    d.nome AS departamento,
    f.data_inicio,
    f.data_fim,
    CURRENT_DATE - f.data_inicio AS dias_para_inicio,
    f.data_fim - f.data_inicio AS dias_ferias
FROM core_ferias f
JOIN core_funcionario func ON f.funcionario_id = func.id
JOIN core_departamento d ON func.departamento_id = d.id
WHERE f.data_inicio BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
ORDER BY f.data_inicio;

-- Uso:
SELECT * FROM vw_ferias_proximas;
```

---

## Estatísticas do Banco

### Tamanho do Banco
```sql
SELECT 
    datname AS database,
    pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
WHERE datname = 'rh_system';
```

### Registros por Tabela
```sql
SELECT 
    schemaname,
    tablename,
    n_live_tup AS registros
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;
```

---

## Relatórios Analíticos

### Folha de Pagamento
```sql
SELECT 
    d.nome AS departamento,
    COUNT(f.id) AS qtd_funcionarios,
    SUM(f.salario) AS total_folha,
    AVG(f.salario) AS salario_medio,
    MAX(f.salario) AS salario_maximo,
    MIN(f.salario) AS salario_minimo
FROM core_departamento d
LEFT JOIN core_funcionario f ON d.id = f.departamento_id
GROUP BY d.nome
ORDER BY total_folha DESC;
```

### Funcionários em Férias (Dashboard)
```sql
SELECT 
    CURRENT_DATE AS data_consulta,
    COUNT(DISTINCT f.id) AS qtd_funcionarios_ferias,
    STRING_AGG(f.nome, ', ') AS nomes
FROM core_ferias fc
JOIN core_funcionario f ON fc.funcionario_id = f.id
WHERE fc.data_inicio <= CURRENT_DATE AND fc.data_fim >= CURRENT_DATE;
```

---

**Diagramas gerados em:** Abril 2026
