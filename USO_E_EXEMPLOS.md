# 📚 Guia de Uso e Exemplos Práticos

## 1️⃣ Acessar o Sistema

### Via Navegador

**Sistema RH:** http://127.0.0.1:8000
**Admin Django:** http://127.0.0.1:8000/admin

---

## 2️⃣ Cadastrar Departamentos

### Pelo Admin (http://127.0.0.1:8000/admin)

1. Faça login com admin/admin123
2. Clique em **Departamentos**
3. Clique em **Adicionar Departamento**
4. Preencha:
   - Nome: `Recursos Humanos`
   - Sigla: `RH`
5. Clique em **Salvar**

### Via Django Shell

```bash
python manage.py shell
```

```python
from core.models import Departamento

# Criar departamentos
Departamento.objects.create(nome="Recursos Humanos", sigla="RH")
Departamento.objects.create(nome="Tecnologia", sigla="TI")
Departamento.objects.create(nome="Finanças", sigla="FIN")
Departamento.objects.create(nome="Vendas", sigla="VD")

# Listar todos
Departamento.objects.all()

# Sair
exit()
```

### Via SQL (PostgreSQL)

```sql
INSERT INTO core_departamento (nome, sigla) VALUES
  ('Recursos Humanos', 'RH'),
  ('Tecnologia', 'TI'),
  ('Finanças', 'FIN'),
  ('Vendas', 'VD');

SELECT * FROM core_departamento;
```

---

## 3️⃣ Cadastrar Funcionários

### Pelo Sistema Web (http://127.0.0.1:8000)

1. Clique em **Funcionários** na navbar
2. Clique em **+ Novo Funcionário**
3. Preencha os dados:
   - Nome: `João Silva`
   - CPF: `123.456.789-00`
   - Cargo: `Desenvolvedor Junior`
   - Salário: `3500.00`
   - Data Admissão: `2023-01-15`
   - Departamento: `Tecnologia`
4. Clique em **Salvar**

### Via Django Shell

```bash
python manage.py shell
```

```python
from core.models import Funcionario, Departamento

# Buscar departamento
ti = Departamento.objects.get(sigla="TI")

# Criar funcionário
Funcionario.objects.create(
    nome="João Silva",
    cpf="123.456.789-00",
    cargo="Desenvolvedor Junior",
    salario=3500.00,
    data_admissao="2023-01-15",
    departamento=ti
)

# Listar funcionários da TI
Funcionario.objects.filter(departamento=ti)

exit()
```

### Via SQL

```sql
INSERT INTO core_funcionario (nome, cpf, cargo, salario, data_admissao, departamento_id)
VALUES 
  ('João Silva', '123.456.789-00', 'Dev Junior', 3500.00, '2023-01-15', 2),
  ('Maria Santos', '987.654.321-00', 'Dev Senior', 5500.00, '2022-06-10', 2),
  ('Carlos Oliveira', '456.789.123-00', 'Gerente', 6000.00', '2021-03-20', 3);

SELECT * FROM core_funcionario;
```

---

## 4️⃣ Registrar Férias

### Pelo Sistema Web

1. Clique em **Férias** na navbar
2. Clique em **+ Registrar Férias**
3. Preencha:
   - Funcionário: `João Silva`
   - Data Início: `2026-07-01`
   - Data Fim: `2026-07-15`
4. Clique em **Salvar**

### Via Django Shell

```bash
python manage.py shell
```

```python
from core.models import Ferias, Funcionario
from datetime import date

joao = Funcionario.objects.get(nome="João Silva")

Ferias.objects.create(
    funcionario=joao,
    data_inicio=date(2026, 7, 1),
    data_fim=date(2026, 7, 15)
)

# Listar férias
Ferias.objects.all()

exit()
```

---

## 5️⃣ Consultas Úteis com Django ORM

### Listar Funcionários por Departamento

```python
from core.models import Funcionario, Departamento

ti = Departamento.objects.get(sigla="TI")
funcionarios = Funcionario.objects.filter(departamento=ti).order_by('nome')

for func in funcionarios:
    print(f"{func.nome} - {func.cargo} - R$ {func.salario}")
```

### Calcular Folha de Pagamento

```python
from django.db.models import Sum

departamentos = Departamento.objects.all()

for dept in departamentos:
    folha = Funcionario.objects.filter(
        departamento=dept
    ).aggregate(total=Sum('salario'))['total'] or 0
    
    print(f"{dept.nome}: R$ {folha:.2f}")
```

### Funcionários em Férias Hoje

```python
from core.models import Ferias
from datetime import date

hoje = date.today()

em_ferias = Ferias.objects.filter(
    data_inicio__lte=hoje,
    data_fim__gte=hoje
).select_related('funcionario', 'funcionario__departamento')

for ferias in em_ferias:
    func = ferias.funcionario
    print(f"{func.nome} ({func.departamento.nome}) - até {ferias.data_fim}")
```

### Tempo de Empresa

```python
from core.models import Funcionario
from datetime import date
from django.db.models import F
from django.db.models.functions import TruncDate

funcionarios = Funcionario.objects.all()

for func in funcionarios:
    dias = (date.today() - func.data_admissao).days
    anos = dias / 365.25
    print(f"{func.nome}: {dias} dias ({anos:.1f} anos)")
```

---

## 6️⃣ Filtros e Buscas no Sistema

### Buscar Funcionário por Nome

No site, vá para **Funcionários** e use a barra de busca:
- Digite: `João`
- Resultado: Todos os funcionários com "João" no nome

### Filtrar por Departamento

Na página de **Funcionários**:
1. Selecione um departamento no dropdown
2. Clique em **Filtrar**
3. Veja apenas funcionários daquele departamento

### Buscar Férias por Funcionário

Na página de **Férias**:
1. Digite o nome do funcionário no campo de busca
2. Pressione Enter ou clique em Filtrar
3. Veja todas as férias daquele funcionário

---

## 7️⃣ Consultas SQL Avançadas

### Folha de Pagamento por Departamento

```sql
SELECT 
    d.nome AS departamento,
    COUNT(f.id) AS qtd_funcionarios,
    SUM(f.salario) AS total_mensal,
    SUM(f.salario) * 12 AS total_anual,
    AVG(f.salario) AS salario_medio,
    MAX(f.salario) AS salario_maximo,
    MIN(f.salario) AS salario_minimo
FROM core_departamento d
LEFT JOIN core_funcionario f ON d.id = f.departamento_id
GROUP BY d.id, d.nome
ORDER BY total_mensal DESC;
```

**Resultado esperado:**
```
departamento | qtd_funcionarios | total_mensal | total_anual | salario_medio | salario_maximo | salario_minimo
─────────────|──────────────────|──────────────|─────────────|───────────────|────────────────|────────────────
Tecnologia   |        2         |    9000.00   | 108000.00   |    4500.00    |   5500.00      |   3500.00
Finanças     |        1         |    6000.00   |  72000.00   |    6000.00    |   6000.00      |   6000.00
```

### Funcionários com Mais de 2 Anos de Empresa

```sql
SELECT 
    f.nome,
    f.cargo,
    f.data_admissao,
    CURRENT_DATE - f.data_admissao AS dias,
    ROUND((CURRENT_DATE - f.data_admissao)::numeric / 365.25, 1) AS anos
FROM core_funcionario f
WHERE (CURRENT_DATE - f.data_admissao) > 730  -- > 2 anos
ORDER BY f.data_admissao;
```

### Funcionários em Férias (Próximos 30 Dias)

```sql
SELECT 
    f.nome,
    d.nome AS departamento,
    fc.data_inicio,
    fc.data_fim,
    fc.data_fim - fc.data_inicio AS dias_ferias
FROM core_ferias fc
JOIN core_funcionario f ON fc.funcionario_id = f.id
JOIN core_departamento d ON f.departamento_id = d.id
WHERE fc.data_inicio BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
ORDER BY fc.data_inicio;
```

### Departamento com Maior Folha

```sql
SELECT 
    d.nome,
    SUM(f.salario) AS total_folha
FROM core_departamento d
JOIN core_funcionario f ON d.id = f.departamento_id
GROUP BY d.id, d.nome
ORDER BY total_folha DESC
LIMIT 1;
```

### Funcionários Sem Férias Programadas

```sql
SELECT 
    f.id,
    f.nome,
    f.cargo,
    d.nome AS departamento
FROM core_funcionario f
LEFT JOIN core_ferias fc ON f.id = fc.funcionario_id
JOIN core_departamento d ON f.departamento_id = d.id
WHERE fc.id IS NULL
ORDER BY f.nome;
```

---

## 8️⃣ Dashboard Django Admin

### Recursos Disponíveis

1. **DEPARTAMENTOS**
   - Visualizar total de funcionários por depto
   - Filtrar por nome/sigla
   - Exportar dados

2. **FUNCIONÁRIOS**
   - Filtras por departamento e data de admissão
   - Ver salário formatado
   - Visualizar salário anual automático
   - Ver tempo na empresa

3. **FÉRIAS**
   - Filtrar por data e departamento
   - Ver número de dias de férias
   - Status (Planejadas/Em andamento/Finalizada)

---

## 9️⃣ Backups e Restauração

### Fazer Backup do PostgreSQL

```powershell
docker exec postgres_rh pg_dump -U rh_user -d rh_system > backup_rh_$(Get-Date -Format 'yyyy-MM-dd').sql
```

### Restaurar Backup

```powershell
docker exec -i postgres_rh psql -U rh_user -d rh_system < backup_rh_2026-04-08.sql
```

### Exportar Dados como JSON

```bash
python manage.py dumpdata core > dados_rh.json
```

### Importar Dados

```bash
python manage.py loaddata dados_rh.json
```

---

## 🔟 Troubleshooting

### Erro ao Buscar Funcionários

```
ValueError: invalid literal for int()
```

**Solução:** Limpe o cache:
```bash
python manage.py clear_cache
```

### Férias com Data Inválida

```
ValidationError: A data de término deve ser após a data de início.
```

**Solução:** Verifique:
- data_fim > data_inicio
- (data_fim - data_inicio) ≤ 30 dias

### Departamento Não Pode Ser Deletado

```
ProtectedError: Não é possível deletar este departamento.
```

**Motivo:** Existem funcionários vinculados  
**Solução:** Mude os funcionários para outro depto ou delete-os primeiro

---

## 📊 Relatórios Úteis

### Gerar Relatório de Funcionários em Férias

```bash
python manage.py shell
```

```python
from core.models import Ferias
from datetime import date, timedelta

hoje = date.today()
proximo_mes = hoje + timedelta(days=30)

ferias_proximas = Ferias.objects.filter(
    data_inicio__gte=hoje,
    data_inicio__lte=proximo_mes
).select_related('funcionario', 'funcionario__departamento').order_by('data_inicio')

print(f"{'Funcionário':<20} {'Depto':<15} {'Início':<12} {'Fim':<12} {'Dias':<6}")
print("=" * 65)

for f in ferias_proximas:
    funcionario = f.funcionario
    dias = (f.data_fim - f.data_inicio).days
    print(f"{funcionario.nome:<20} {funcionario.departamento.sigla:<15} {f.data_inicio} {f.data_fim} {dias:<6}")

exit()
```

---

**Documentação criada em:** Abril 2026
