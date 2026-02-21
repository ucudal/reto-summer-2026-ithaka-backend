"""
API Router Principal
====================
Este archivo AGRUPA todos los routers de los endpoints.

Cuando creen un nuevo archivo de endpoints (ej: casos.py), deben:
1. Importarlo aquí
2. Incluirlo con api_router.include_router()

Así todos los endpoints quedan bajo /api/v1/
"""

from fastapi import APIRouter

# Importar los routers de cada endpoint
from app.api.v1.endpoints import (
    apoyo,
    apoyo_solicitado,
    asignacion,
    auditoria,
    caso,
    catalogo_estados,
    convocatoria,
    emprendedores,
    nota,
    programa,
    rol,
    usuario,
    auth
)

# Router principal que agrupa todo
api_router = APIRouter()

# ============================================================================
# INCLUIR TODOS LOS ROUTERS
# ============================================================================

# Emprendedores
api_router.include_router(
    emprendedores.router,
    prefix="/emprendedores",
    tags=["emprendedores"]
)

# Catálogo de Estados
api_router.include_router(
    catalogo_estados.router,
    prefix="/estados",
    tags=["estados"]
)

# Casos
api_router.include_router(
    caso.router,
    prefix="/casos",
    tags=["casos"]
)

# Notas
api_router.include_router(
    nota.router,
    prefix="/notas",
    tags=["notas"]
)

# Auditoría
api_router.include_router(
    auditoria.router,
    prefix="/auditoria",
    tags=["auditoria"]
)

# Convocatorias
api_router.include_router(
    convocatoria.router,
    prefix="/convocatorias",
    tags=["convocatorias"]
)

# Programas
api_router.include_router(
    programa.router,
    prefix="/programas",
    tags=["programas"]
)

# Autenticación
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["autenticación"]
)

# Usuarios
api_router.include_router(
    usuario.router,
    prefix="/usuarios",
    tags=["usuarios"]
)

# Roles
api_router.include_router(
    rol.router,
    prefix="/roles",
    tags=["roles"]
)

# Asignaciones
api_router.include_router(
    asignacion.router,
    prefix="/asignaciones",
    tags=["asignaciones"]
)

# Apoyos
api_router.include_router(
    apoyo.router,
    prefix="/apoyos",
    tags=["apoyos"]
)

# Apoyos Solicitados
api_router.include_router(
    apoyo_solicitado.router,
    prefix="/apoyos-solicitados",
    tags=["apoyos-solicitados"]
)

# ============================================================================
# RESULTADO FINAL
# ============================================================================
# Si tienes:
#   - emprendedores.py con un endpoint GET "/"
#   - casos.py con un endpoint POST "/"
#
# Las URLs finales serán:
#   - GET  /api/v1/emprendedores/
#   - POST /api/v1/casos/
#
# El main.py incluye este api_router con prefix="/api/v1"
