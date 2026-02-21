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
    tipo_apoyo: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Tipo de apoyo otorgado",
        examples=["Mentoría", "Incubación inicial", "Financiamiento"]
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
    pass


class ApoyoUpdate(BaseModel):
    """Schema para actualizar apoyo"""
    tipo_apoyo: Optional[str] = Field(None, min_length=1, max_length=150)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_caso: Optional[int] = None
    id_programa: Optional[int] = None


class ApoyoResponse(ApoyoBase):
    """Schema para respuesta"""
    id_apoyo: int
    
    class Config:
        from_attributes = True
