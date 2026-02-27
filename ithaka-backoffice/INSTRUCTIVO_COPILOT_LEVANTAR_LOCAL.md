# Instructivo para levantar Ithaka Backoffice con Copilot

Este documento está pensado para que cualquier compañero copie y pegue prompts en Copilot Chat (modo Agent) y levante la API + base local para probar endpoints.

## 1. Prerrequisitos

1. Tener Docker Desktop abierto.
2. Tener VS Code con Copilot Chat en modo Agent.
3. Abrir esta carpeta en VS Code: `reto-summer-2026-ithaka-backend/ithaka-backoffice`.

## 2. Prompt para preparar entorno

Pegar en Copilot:

```text
Parate en la carpeta del proyecto (ithaka-backoffice), mostrame pwd y git branch actual, y luego dejá un archivo .env con este contenido exacto:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ithaka_db
POSTGRES_SERVER=localhost
POSTGRES_PORT=50001
SECRET_KEY=desarrollo-inseguro-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_NAME=Ithaka Backoffice
VERSION=1.0.0
ENVIRONMENT=development
```

## 3. Prompt para levantar contenedores limpios

Pegar en Copilot:

```text
Ejecutá estos comandos en orden y mostrame la salida:
docker compose down -v --remove-orphans
docker compose up -d --build
docker compose ps
```

Resultado esperado:
- Contenedor `ithaka_postgres` en `healthy`.
- Contenedor `ithaka_api` en `Up`.

## 4. Prompt para cargar esquema y datos base

Pegar en Copilot:

```text
Ejecutá estos comandos en orden y mostrame la salida:
docker exec -i ithaka_postgres psql -U postgres -d ithaka_db < ithaka_backoffice.sql
docker exec -i ithaka_postgres psql -U postgres -d ithaka_db < ithakaInsertsTest.sql
docker exec ithaka_api python -m scripts.create_test_users
```

## 5. Prompt para validar que quedó funcionando

Pegar en Copilot:

```text
Validá la API con estos checks y mostrame resultados:
curl -i http://localhost:8000/health
curl -s -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d '{"email":"admin@ithaka.com","password":"admin123"}'
```

Resultado esperado:
- `/health` responde `200`.
- Login devuelve `access_token`.

## 6. Credenciales de prueba

- `admin@ithaka.com / admin123`
- `coordinador@ithaka.com / coord123`
- `tutor1@ithaka.com / tutor123`
- `tutor2@ithaka.com / tutor123`

## 7. URL para probar endpoints

- Swagger: `http://localhost:8000/docs`

## 8. Si algo falla

1. Pedile a Copilot: `mostrame docker compose logs --tail 120 api db`.
2. Si hay errores de datos duplicados o credenciales viejas, repetir desde el paso 3 (`down -v` y carga completa otra vez).
