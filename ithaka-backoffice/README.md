# Ithaka Backoffice API

API mínima para el proyecto de gestión de postulaciones del Centro de Emprendimiento e Innovación - Universidad Católica del Uruguay.

## Descripción

Esta es una API FastAPI mínima que proporciona endpoints básicos para:
- Crear postulaciones desde el chatbot
- Listar postulaciones con filtros
- Obtener detalles de postulaciones específicas
- Consultar estadísticas básicas

## Requisitos

- Python 3.11+
- pip

## Instalación y Ejecución Local

### Opción 1: Entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload
```

### Opción 2: Docker

```bash
# Construir imagen
docker build -t ithaka-backoffice .

# Ejecutar contenedor
docker run -p 8000:8000 ithaka-backoffice
```

## Endpoints Disponibles

Una vez ejecutado, la API estará disponible en `http://localhost:8000`

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

- `GET /` - Health check y información de la API
- `GET /health` - Estado de salud del servicio
- `POST /api/postulaciones` - Crear nueva postulación
- `GET /api/postulaciones` - Listar postulaciones (con filtro opcional por estado)
- `GET /api/postulaciones/{id}` - Obtener detalle de una postulación
- `GET /api/stats` - Obtener estadísticas básicas

## Ejemplo de Uso

### Crear una postulación

```bash
curl -X POST "http://localhost:8000/api/postulaciones" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_emprendedor": "Juan Pérez",
    "email": "juan.perez@example.com",
    "telefono": "+598 99 123 456",
    "nombre_idea": "EcoApp",
    "descripcion": "Aplicación para gestión de residuos",
    "vinculo_institucional": "Estudiante UCU"
  }'
```

### Listar postulaciones

```bash
curl "http://localhost:8000/api/postulaciones"
```

### Filtrar por estado

```bash
curl "http://localhost:8000/api/postulaciones?estado=recibida"
```

### Obtener estadísticas

```bash
curl "http://localhost:8000/api/stats"
```

## Estados de Postulación

- `borrador` - Postulación iniciada pero no completada
- `recibida` - Postulación recibida y pendiente de revisión
- `en_revision` - En proceso de evaluación
- `aprobada` - Postulación aprobada
- `rechazada` - Postulación rechazada

## Notas Técnicas

- Esta es una versión mínima con base de datos en memoria
- Los datos se pierden al reiniciar el servidor
- Para producción, se debe integrar con base de datos persistente (PostgreSQL, MongoDB, etc.)
- La autenticación y autorización (RBAC) se implementará en fases posteriores

## Próximos Pasos

1. Integración con base de datos persistente
2. Sistema de autenticación y roles (RBAC)
3. Asignación de tutores
4. Auditoría de cambios
5. Reportes avanzados y exportación
6. Integración completa con el chatbot

## Estructura inicial del Proyecto

```
ithaka-backoffice/
├── main.py              # Aplicación FastAPI principal
├── requirements.txt     # Dependencias Python
├── Dockerfile          # Configuración Docker
├── .dockerignore       # Archivos a ignorar en Docker
├── .gitignore          # Archivos a ignorar en Git
└── README.md           # Este archivo
```

## Contacto

Centro de Emprendimiento e Innovación - Universidad Católica del Uruguay


## Estructura recomendada

ithaka-backoffice/
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/                    # Configuración central
│   │   ├── __init__.py
│   │   ├── config.py            # Variables de entorno, configuración DB
│   │   └── security.py          # Funciones de autenticación/JWT
│   │
│   ├── db/                      # Base de datos
│   │   ├── __init__.py
│   │   ├── database.py          # Conexión a PostgreSQL (SQLAlchemy)
│   │   └── session.py           # Dependency para obtener sesiones DB
│   │
│   ├── models/                  # Modelos SQLAlchemy (tablas DB)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── emprendedor.py
│   │   ├── caso.py
│   │   ├── convocatoria.py
│   │   ├── programa.py
│   │   ├── apoyo.py
│   │   ├── asignacion.py
│   │   ├── nota.py
│   │   ├── auditoria.py
│   │   └── catalogo_estados.py
│   │
│   ├── schemas/                 # Schemas Pydantic (validación API)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── emprendedor.py
│   │   ├── caso.py
│   │   ├── convocatoria.py
│   │   ├── programa.py
│   │   └── ...
│   │
│   ├── api/                     # Endpoints
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependencies compartidas
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py           # Agrupa todos los routers
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py      # Login, logout
│   │           ├── usuarios.py
│   │           ├── emprendedores.py
│   │           ├── casos.py
│   │           ├── convocatorias.py
│   │           ├── programas.py
│   │           └── ...
│   │
│   └── services/                # Lógica de negocio (opcional pero recomendado)
│       ├── __init__.py
│       ├── caso_service.py
│       ├── auditoria_service.py
│       └── ...
│
├── alembic/                     # Migraciones de base de datos
│   └── versions/
│
├── tests/                       # Tests
│   ├── __init__.py
│   └── test_api/
│
├── .env                         # Variables de entorno (NO subir a git)
├── .env.example                 # Ejemplo de variables
├── alembic.ini                  # Configuración de migraciones
├── requirements.txt
├── main.py                      # Punto de entrada
└── README.md