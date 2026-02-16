"""
Schemas CATALOGO_ESTADOS
-------------------------
Define los estados posibles de los casos.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class CatalogoEstadosBase(BaseModel):
    """Campos comunes de estados"""
    nombre_estado: str = Field(
        ...,
        max_length=100,
        description="Nombre del estado",
        examples=["En Revisión", "Aprobado", "Rechazado"]
    )
    
    tipo_caso: Literal["Postulacion", "Proyecto"] = Field(
        ...,
        description="Tipo de caso al que aplica este estado"
    )


class CatalogoEstadosCreate(CatalogoEstadosBase):
    """Schema para crear estado (POST)"""
    pass


class CatalogoEstadosUpdate(BaseModel):
    """Schema para actualizar estado (PUT)"""
    nombre_estado: Optional[str] = Field(None, max_length=100)
    tipo_caso: Optional[Literal["Postulacion", "Proyecto"]] = None


class CatalogoEstadosResponse(CatalogoEstadosBase):
    """Schema para respuesta (GET)"""
    id_estado: int = Field(..., description="ID único del estado")
    
    class Config:
        from_attributes = True
