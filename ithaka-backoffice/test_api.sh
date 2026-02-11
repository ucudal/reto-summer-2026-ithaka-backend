#!/bin/bash

echo "=== Ithaka Backoffice API - Script de Prueba ==="
echo ""
echo "1. Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "2. Iniciando servidor (en background)..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

echo "Esperando que el servidor inicie..."
sleep 3

echo ""
echo "3. Probando endpoints..."
echo ""

echo "Health Check:"
curl -s http://localhost:8000/health | python -m json.tool
echo ""

echo "Creando postulación de prueba..."
curl -s -X POST "http://localhost:8000/api/postulaciones" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_emprendedor": "María González",
    "email": "maria.gonzalez@ucu.edu.uy",
    "telefono": "+598 99 123 456",
    "nombre_idea": "GreenTech Solutions",
    "descripcion": "Plataforma para conectar emprendimientos sustentables con inversores",
    "vinculo_institucional": "Egresada UCU"
  }' | python -m json.tool
echo ""

echo "Listando todas las postulaciones..."
curl -s http://localhost:8000/api/postulaciones | python -m json.tool
echo ""

echo "Obteniendo estadísticas..."
curl -s http://localhost:8000/api/stats | python -m json.tool
echo ""

echo "4. Deteniendo servidor..."
kill $SERVER_PID

echo ""
echo "=== Prueba completada ==="
echo "Para usar la API:"
echo "  1. uvicorn main:app --reload"
echo "  2. Abre http://localhost:8000/docs para ver la documentación interactiva"
