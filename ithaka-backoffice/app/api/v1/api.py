from fastapi import APIRouter

from app.api.v1.endpoints import (
    emprendedores,
    catalogo_estados,
    caso,
    convocatoria,
    programa,
    roles,
    auth,
    usuarios,
)

api_router = APIRouter()

api_router.include_router(emprendedores.router,    prefix="/emprendedores",  tags=["emprendedores"])
api_router.include_router(catalogo_estados.router, prefix="/estados",        tags=["estados"])
api_router.include_router(caso.router,             prefix="/casos",          tags=["casos"])
api_router.include_router(convocatoria.router,     prefix="/convocatorias",  tags=["convocatorias"])
api_router.include_router(programa.router,         prefix="/programas",      tags=["programas"])
api_router.include_router(roles.router,            prefix="/roles",          tags=["roles"])
api_router.include_router(auth.router,             prefix="/auth",           tags=["autenticación"])
api_router.include_router(usuarios.router,         prefix="/usuarios",       tags=["usuarios"])