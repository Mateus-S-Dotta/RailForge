Start-Process "$Env:ProgramFiles\Docker\Docker\Docker Desktop.exe"

Write-Host "Aguardando o Docker iniciar..."

# Espera até o Docker responder
while ($true) {
    try {
        docker info *> $null
        break
    }
    catch {
        Start-Sleep -Seconds 2
    }
}

Write-Host "Docker está pronto!"

$ErrorActionPreference = "Stop"

$rootPath = $PSScriptRoot
$bdPath = Join-Path $rootPath "bd"
$apiPath = Join-Path $rootPath "api"

Write-Host "==> Subindo o banco de dados..." -ForegroundColor Cyan
Set-Location $bdPath
docker compose up -d

Write-Host "==> Aguardando o banco ficar saudavel..." -ForegroundColor Cyan
$maxTries = 30
$tries = 0
$healthy = $false

while ($tries -lt $maxTries) {
    $status = docker inspect --format='{{.State.Health.Status}}' postgress 2>$null

    if ($status -eq "healthy") {
        $healthy = $true
        break
    }

    Start-Sleep -Seconds 2
    $tries++
    Write-Host "   Aguardando... ($tries/$maxTries)" -ForegroundColor DarkGray
}

if (-not $healthy) {
    Write-Host "==> ERRO: o banco nao ficou saudavel a tempo." -ForegroundColor Red
    exit 1
}

Write-Host "==> Banco pronto!" -ForegroundColor Green

Write-Host "==> Subindo a API..." -ForegroundColor Cyan
Set-Location $apiPath
docker compose up -d --build

Write-Host "==> Tudo no ar! API disponivel em http://localhost:8000" -ForegroundColor Green

Set-Location $rootPath