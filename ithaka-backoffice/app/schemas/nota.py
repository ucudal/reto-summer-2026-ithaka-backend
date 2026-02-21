"""
Schemas NOTA
------------
TODO: Implementar usando TEMPLATE.py como guía

Campos según SQL:
- id_nota (solo en Response)
- contenido
- fecha (autogenerado)
- id_usuario
- id_caso
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NotaBase(BaseModel):
    contenido: str = Field(
        ...,
        min_length=1,
        description="Contenido de la nota"
    )
    id_usuario: int = Field(
        ...,
        description="ID del usuario que registra la nota"
    )
    id_caso: int = Field(
        ...,
        description="ID del caso asociado"
    )


class NotaCreate(NotaBase):
    pass


class NotaUpdate(BaseModel):
    contenido: Optional[str] = Field(None, min_length=1)
    id_usuario: Optional[int] = None
    id_caso: Optional[int] = None


class NotaResponse(NotaBase):
    id_nota: int = Field(..., description="ID único de la nota")
    fecha: datetime = Field(..., description="Fecha de creación de la nota")

    class Config:
        from_attributes = True
