"""
MAIN.PY - Punto de Entrada de la Aplicación
============================================

Este es el archivo principal que:
1. Crea la aplicación FastAPI
2. Configura CORS y middleware
3. Incluye los routers de la API
4. Define endpoints básicos (root, health)

Para ejecutar:
    uvicorn main:app --reload
    
Documentación interactiva:
    http://localhost:8000/docs    (Swagger UI)
    http://localhost:8000/redoc   (ReDoc)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar el router principal de la API v1
from app.api.v1.api import api_router

# ============================================================================
# CREAR APLICACIÓN FASTAPI
# ============================================================================
app = FastAPI(
    title="Ithaka Backoffice API",
    description="API para gestión de postulaciones y proyectos del Centro de Emprendimiento e Innovación - UCU",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc
)

# ============================================================================
# CONFIGURAR CORS
# ============================================================================
# CORS permite que el frontend (en otro dominio) pueda llamar a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # En producción: ["https://tu-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],        # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Permite todos los headers
)

# ============================================================================
# INCLUIR ROUTERS DE LA API
# ============================================================================
# Todos los endpoints de la API estarán bajo /api/v1
# Ejemplo: /api/v1/emprendedores, /api/v1/casos, etc.
app.include_router(
    api_router,
    prefix="/api/v1"  # Prefijo para todos los endpoints
)

# ============================================================================
# ENDPOINTS BÁSICOS (ROOT Y HEALTH CHECK)
# ============================================================================
@app.get("/")
def root():
    """
    Endpoint raíz - Información básica de la API
    
    URL: GET /
    
    Returns: Información sobre la API y links útiles
    """
    return {
        "message": "Ithaka Backoffice API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_v1": "/api/v1"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint - Verificar que la API está funcionando
    
    URL: GET /health
    
    Returns: Estado de salud del servicio
    
    Útil para:
    - Monitoreo del servidor
    - Load balancers
    - Docker health checks
    """
    return {
        "status": "healthy",
        "service": "ithaka-backoffice"
    }


# ============================================================================
# NOTA PARA EL EQUIPO
# ============================================================================
# 
# Este archivo NO debe tener endpoints de negocio.
# Solo:
#   - Configuración de la app
#   - Middleware
#   - Inclusión de routers
#   - Endpoints básicos (root, health)
# 
# Para agregar endpoints de negocio:
#   1. Crear archivo en app/api/v1/endpoints/
#   2. Importar el router en app/api/v1/api.py
#   3. Incluirlo con api_router.include_router()
# 
# Para más información, ver: GUIA_ENDPOINTS.md
# ============================================================================
