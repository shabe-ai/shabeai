param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Green
    Write-Host "  dev          - Start development environment with hot reloading" -ForegroundColor Cyan
    Write-Host "  build        - Build all Docker images" -ForegroundColor Cyan
    Write-Host "  up           - Start production environment" -ForegroundColor Cyan
    Write-Host "  down         - Stop all containers" -ForegroundColor Cyan
    Write-Host "  logs         - Show logs from all services" -ForegroundColor Cyan
    Write-Host "  logs-backend - Show backend logs" -ForegroundColor Cyan
    Write-Host "  logs-frontend- Show frontend logs" -ForegroundColor Cyan
    Write-Host "  clean        - Remove all containers, networks, and volumes" -ForegroundColor Cyan
    Write-Host "  test         - Run backend tests" -ForegroundColor Cyan
    Write-Host "  test-frontend- Run frontend tests" -ForegroundColor Cyan
    Write-Host "  lint         - Run backend linting" -ForegroundColor Cyan
    Write-Host "  db-migrate   - Run database migrations" -ForegroundColor Cyan
    Write-Host "  db-reset     - Reset database (WARNING: This will delete all data)" -ForegroundColor Cyan
}

function Start-Dev {
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
}

function Build-Images {
    docker-compose build
}

function Start-Production {
    docker-compose up -d
}

function Stop-Containers {
    docker-compose down
}

function Show-Logs {
    docker-compose logs -f
}

function Show-BackendLogs {
    docker-compose logs -f backend
}

function Show-FrontendLogs {
    docker-compose logs -f frontend
}

function Clean-All {
    docker-compose down -v --remove-orphans
    docker system prune -f
}

function Run-Tests {
    Set-Location backend
    python -m pytest tests/ -v
    Set-Location ..
}

function Run-FrontendTests {
    Set-Location frontend
    pnpm test
    Set-Location ..
}

function Run-Lint {
    Set-Location backend
    ruff check .
    ruff format .
    Set-Location ..
}

function Run-DbMigrate {
    Set-Location backend
    alembic upgrade head
    Set-Location ..
}

function Reset-Database {
    Write-Host "WARNING: This will delete all data!" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (y/N)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        docker-compose down -v
        docker-compose up postgres -d
        Start-Sleep -Seconds 5
        Set-Location backend
        alembic upgrade head
        Set-Location ..
    }
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "dev" { Start-Dev }
    "build" { Build-Images }
    "up" { Start-Production }
    "down" { Stop-Containers }
    "logs" { Show-Logs }
    "logs-backend" { Show-BackendLogs }
    "logs-frontend" { Show-FrontendLogs }
    "clean" { Clean-All }
    "test" { Run-Tests }
    "test-frontend" { Run-FrontendTests }
    "lint" { Run-Lint }
    "db-migrate" { Run-DbMigrate }
    "db-reset" { Reset-Database }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help
    }
} 