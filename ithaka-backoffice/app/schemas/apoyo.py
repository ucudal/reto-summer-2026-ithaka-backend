"""
Schemas APOYO
-------------
Validaciones para apoyos otorgados a casos.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class ApoyoBase(BaseModel):
    """Campos comunes de apoyo"""
    id_catalogo_apoyo: int = Field(
        ...,
        description="ID del catálogo de apoyo"
    )
    
    fecha_inicio: Optional[date] = Field(
        None,
        description="Fecha de inicio del apoyo"
    )
    
    fecha_fin: Optional[date] = Field(
        None,
        description="Fecha de fin del apoyo"
    )
    
    id_caso: int = Field(
        ...,
        description="ID del caso que recibe el apoyo"
    )
    
    id_programa: int = Field(
        ...,
        description="ID del programa que otorga el apoyo"
    )


class ApoyoCreate(ApoyoBase):
    """Schema para crear apoyo"""
    class Config:
        json_schema_extra = {
            "example": {
                "id_catalogo_apoyo": 1,
                "fecha_inicio": "2026-03-01",
                "fecha_fin": "2026-04-01",
                "id_caso": 2,
                "id_programa": 3
            }
        }


class ApoyoUpdate(BaseModel):
    """Schema para actualizar apoyo"""
    id_catalogo_apoyo: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_caso: Optional[int] = None
    id_programa: Optional[int] = None


class ApoyoResponse(ApoyoBase):
    """Schema para respuesta"""
    id_apoyo: int
    
    class Config:
        from_attributes = True
