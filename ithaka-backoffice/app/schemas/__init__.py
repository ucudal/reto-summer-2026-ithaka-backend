"""
Schemas de Pydantic
-------------------
Importa todos los schemas para facilitar su uso
"""

# Emprendedor
from app.schemas.emprendedor import (
    EmprendedorBase,
    EmprendedorCreate,
    EmprendedorUpdate,
    EmprendedorResponse,
    EmprendedorListResponse
)

# Catálogo de Estados
from app.schemas.catalogo_estados import (
    CatalogoEstadosBase,
    CatalogoEstadosCreate,
    CatalogoEstadosUpdate,
    CatalogoEstadosResponse
)

# Caso
from app.schemas.caso import (
    CasoBase,
    CasoCreate,
    CasoUpdate,
    CasoResponse
)

# Nota
from app.schemas.nota import (
    NotaBase,
    NotaCreate,
    NotaUpdate,
    NotaResponse
)

# Auditoría
from app.schemas.auditoria import (
    AuditoriaBase,
    AuditoriaCreate,
    AuditoriaUpdate,
    AuditoriaResponse
)

__all__ = [
    # Emprendedor
    "EmprendedorBase",
    "EmprendedorCreate",
    "EmprendedorUpdate",
    "EmprendedorResponse",
    "EmprendedorListResponse",
    # Catálogo Estados
    "CatalogoEstadosBase",
    "CatalogoEstadosCreate",
    "CatalogoEstadosUpdate",
    "CatalogoEstadosResponse",
    # Caso
    "CasoBase",
    "CasoCreate",
    "CasoUpdate",
    "CasoResponse",
    # Nota
    "NotaBase",
    "NotaCreate",
    "NotaUpdate",
    "NotaResponse",
    # Auditoría
    "AuditoriaBase",
    "AuditoriaCreate",
    "AuditoriaUpdate",
    "AuditoriaResponse",
]
