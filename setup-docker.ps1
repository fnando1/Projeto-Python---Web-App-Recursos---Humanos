# Script para inicializar o sistema RH com PostgreSQL via Docker
# Execute este script em PowerShell como Administrador

Write-Host "==================================" -ForegroundColor Green
Write-Host "  Sistema RH - Setup Docker PostgreSQL" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""

# Verificar se Docker está instalado
Write-Host "[1/5] Verificando Docker..." -ForegroundColor Cyan
try {
    docker --version | Out-Null
    Write-Host "✓ Docker encontrado" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker não está instalado!" -ForegroundColor Red
    Write-Host "Instale Docker Desktop em: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Iniciar PostgreSQL via docker-compose
Write-Host ""
Write-Host "[2/5] Iniciando PostgreSQL com Docker..." -ForegroundColor Cyan
docker-compose up -d

# Aguardar container ficar pronto
Write-Host "⏳ Aguardando PostgreSQL ficar pronto..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Ativar ambiente virtual
Write-Host ""
Write-Host "[3/5] Ativando ambiente virtual..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Configurar variáveis de ambiente
Write-Host ""
Write-Host "[4/5] Configurando variáveis de ambiente..." -ForegroundColor Cyan
$env:DJANGO_USE_POSTGRES="1"
$env:POSTGRES_DB="rh_system"
$env:POSTGRES_USER="rh_user"
$env:POSTGRES_PASSWORD="senha_segura_123"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"

Write-Host "✓ Variáveis configuradas" -ForegroundColor Green

# Executar migrações
Write-Host ""
Write-Host "[5/5] Executando migrações..." -ForegroundColor Cyan
python manage.py migrate

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "  ✓ Sistema configurado com sucesso!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Criar superusuário: python manage.py createsuperuser" -ForegroundColor White
Write-Host "2. Iniciar servidor: python manage.py runserver" -ForegroundColor White
Write-Host "3. Acessar: http://127.0.0.1:8000" -ForegroundColor White
Write-Host ""
