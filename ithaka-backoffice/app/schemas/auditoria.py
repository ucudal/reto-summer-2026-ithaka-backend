"""
Schemas AUDITORIA
-----------------
TODO: Implementar usando TEMPLATE.py como guía

Campos según SQL:
- id_auditoria (solo en Response)
- timestamp (autogenerado)
- accion
- valor_anterior
- valor_nuevo
- id_usuario
- id_caso
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AuditoriaBase(BaseModel):
    accion: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Acción registrada en auditoría"
    )
    valor_anterior: Optional[str] = Field(
        None,
        description="Valor previo al cambio"
    )
    valor_nuevo: Optional[str] = Field(
        None,
        description="Valor posterior al cambio"
    )
    id_usuario: int = Field(
        ...,
        description="ID del usuario que realizó la acción"
    )
    id_caso: Optional[int] = Field(
        None,
        description="ID del caso sobre el que se realizó la acción (opcional para auditoría general)"
    )


class AuditoriaCreate(AuditoriaBase):
    pass


class AuditoriaUpdate(BaseModel):
    accion: Optional[str] = Field(None, min_length=1, max_length=150)
    valor_anterior: Optional[str] = None
    valor_nuevo: Optional[str] = None
    id_usuario: Optional[int] = None
    id_caso: Optional[int] = None


class AuditoriaResponse(AuditoriaBase):
    id_auditoria: int = Field(..., description="ID único de auditoría")
    timestamp: datetime = Field(..., description="Fecha/hora del registro")

    class Config:
        from_attributes = True
