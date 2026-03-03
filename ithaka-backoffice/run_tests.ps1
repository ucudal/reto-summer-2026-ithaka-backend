# ==============================================================================
# SCRIPT DE TESTING - ITHAKA BACKOFFICE
# ==============================================================================
# Este script ejecuta los tests con diferentes configuraciones de coverage

Write-Host "🧪 ITHAKA BACKOFFICE - TEST SUITE" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Función para mostrar menú
function Show-Menu {
    Write-Host "Selecciona una opción:" -ForegroundColor Yellow
    Write-Host "1. Ejecutar TODOS los tests"
    Write-Host "2. Ejecutar tests con coverage básico"
    Write-Host "3. Ejecutar tests con coverage detallado"
    Write-Host "4. Generar reporte HTML de coverage"
    Write-Host "5. Ejecutar solo tests rápidos"
    Write-Host "6. Ejecutar tests de un archivo específico"
    Write-Host "7. Ver estadísticas de tests"
    Write-Host "0. Salir"
    Write-Host ""
}

# Loop principal
do {
    Show-Menu
    $option = Read-Host "Opción"
    
    switch ($option) {
        "1" {
            Write-Host "▶️ Ejecutando todos los tests..." -ForegroundColor Green
            pytest -v
        }
        "2" {
            Write-Host "▶️ Ejecutando tests con coverage..." -ForegroundColor Green
            pytest --cov=app --cov-report=term
        }
        "3" {
            Write-Host "▶️ Ejecutando tests con coverage detallado..." -ForegroundColor Green
            pytest --cov=app --cov-report=term-missing
        }
        "4" {
            Write-Host "▶️ Generando reporte HTML..." -ForegroundColor Green
            pytest --cov=app --cov-report=html
            Write-Host "✅ Reporte generado en: htmlcov/index.html" -ForegroundColor Green
            $open = Read-Host "¿Abrir reporte? (s/n)"
            if ($open -eq "s") {
                Start-Process "htmlcov/index.html"
            }
        }
        "5" {
            Write-Host "▶️ Ejecutando solo tests rápidos..." -ForegroundColor Green
            pytest -v -m "not slow"
        }
        "6" {
            Write-Host "Archivos de test disponibles:" -ForegroundColor Yellow
            Get-ChildItem tests\test_*.py | ForEach-Object { Write-Host "  - $($_.Name)" }
            $file = Read-Host "Nombre del archivo (ej: test_casos.py)"
            pytest -v "tests\$file"
        }
        "7" {
            Write-Host "📊 Estadísticas de tests:" -ForegroundColor Cyan
            pytest --collect-only -q
        }
        "0" {
            Write-Host "👋 Hasta luego!" -ForegroundColor Cyan
        }
        default {
            Write-Host "❌ Opción inválida" -ForegroundColor Red
        }
    }
    
    if ($option -ne "0") {
        Write-Host ""
        Read-Host "Presiona Enter para continuar"
        Clear-Host
    }
    
} while ($option -ne "0")
