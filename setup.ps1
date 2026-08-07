Start-Process "$Env:ProgramFiles\Docker\Docker\Docker Desktop.exe"

Write-Host "Aguardando o Docker iniciar..."

# Espera até o Docker responder
while ($true) {
    docker info *> $null
    if ($LASTEXITCODE -eq 0) {
        break
    }
    Start-Sleep -Seconds 2
}

Write-Host "Docker está pronto!"

$ErrorActionPreference = "Stop"

$rootPath = $PSScriptRoot
$bdPath = Join-Path $rootPath "bd"
$apiPath = Join-Path $rootPath "api"
$frontPath = Join-Path $rootPath "frontend"

Write-Host "==> Subindo o banco de dados..." -ForegroundColor Cyan
Set-Location $bdPath
docker compose up -d

Write-Host "==> Aguardando o banco ficar saudavel..." -ForegroundColor Cyan
$maxTries = 30
$tries = 0
$healthy = $false

$containerId = docker compose ps -q db

while ($tries -lt $maxTries) {
    $status = docker inspect --format='{{.State.Health.Status}}' $containerId 2>$null

    if ($status -eq "healthy") {
        $healthy = $true
        break
    }

    Write-Host "Banco ainda nao esta pronto (status: $status). Tentativa $($tries+1)/$maxTries..."
    Start-Sleep -Seconds 2
    $tries++
}

if (-not $healthy) {
    throw "Banco de dados nao ficou saudavel a tempo."
}

Write-Host "==> Banco pronto!" -ForegroundColor Green

Write-Host "==> Subindo a API..." -ForegroundColor Cyan
Set-Location $apiPath
docker compose up -d --build

Write-Host "==> API disponivel em http://localhost:8000" -ForegroundColor Green

Write-Host "==> Subindo a Front..." -ForegroundColor Cyan

Set-Location $frontPath

docker run --rm -it -v "${PWD}:/app" -w /app node:24.14.0-slim npm install
docker compose watch frontend-dev

Write-Host "==> Front disponivel em http://localhost:3000" -ForegroundColor Green
