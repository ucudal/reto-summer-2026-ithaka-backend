#!/bin/bash

# ==============================================================================
# SCRIPT DE TESTING - ITHAKA BACKOFFICE (Bash version)
# ==============================================================================

echo "🧪 ITHAKA BACKOFFICE - TEST SUITE"
echo "=================================="
echo ""

show_menu() {
    echo "Selecciona una opción:"
    echo "1. Ejecutar TODOS los tests"
    echo "2. Ejecutar tests con coverage básico"
    echo "3. Ejecutar tests con coverage detallado"
    echo "4. Generar reporte HTML de coverage"
    echo "5. Ejecutar solo tests rápidos"
    echo "6. Ejecutar tests de un archivo específico"
    echo "7. Ver estadísticas de tests"
    echo "0. Salir"
    echo ""
}

while true; do
    show_menu
    read -p "Opción: " option
    
    case $option in
        1)
            echo "▶️ Ejecutando todos los tests..."
            pytest -v
            ;;
        2)
            echo "▶️ Ejecutando tests con coverage..."
            pytest --cov=app --cov-report=term
            ;;
        3)
            echo "▶️ Ejecutando tests con coverage detallado..."
            pytest --cov=app --cov-report=term-missing
            ;;
        4)
            echo "▶️ Generando reporte HTML..."
            pytest --cov=app --cov-report=html
            echo "✅ Reporte generado en: htmlcov/index.html"
            read -p "¿Abrir reporte? (s/n): " open
            if [ "$open" = "s" ]; then
                xdg-open htmlcov/index.html 2>/dev/null || open htmlcov/index.html
            fi
            ;;
        5)
            echo "▶️ Ejecutando solo tests rápidos..."
            pytest -v -m "not slow"
            ;;
        6)
            echo "Archivos de test disponibles:"
            ls tests/test_*.py | sed 's/tests\//  - /'
            read -p "Nombre del archivo (ej: test_casos.py): " file
            pytest -v "tests/$file"
            ;;
        7)
            echo "📊 Estadísticas de tests:"
            pytest --collect-only -q
            ;;
        0)
            echo "👋 Hasta luego!"
            break
            ;;
        *)
            echo "❌ Opción inválida"
            ;;
    esac
    
    if [ "$option" != "0" ]; then
        echo ""
        read -p "Presiona Enter para continuar..."
        clear
    fi
done
