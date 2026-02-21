"""
Schemas ASIGNACION
------------------
Validación de datos para asignaciones de usuarios a casos.

Campos según SQL:
- id_asignacion (solo en Response)
- fecha_asignacion (autogenerado en DB)
- id_usuario (FK a usuario)
- id_caso (FK a caso)
"""

from pydantic import BaseModel, Field
from datetime import datetime


class AsignacionBase(BaseModel):
    """Campos comunes de asignación"""
    id_usuario: int = Field(
        ...,
        gt=0,
        description="ID del usuario (coordinador/tutor) asignado",
        examples=[1]
    )
    id_caso: int = Field(
        ...,
        gt=0,
        description="ID del caso al que se asigna el usuario",
        examples=[1]
    )


class AsignacionCreate(AsignacionBase):
    """Schema para crear asignación (sin fecha, se genera automáticamente)"""
    pass


class AsignacionUpdate(BaseModel):
    """Schema para actualizar asignación (solo permite cambiar usuario asignado)"""
    id_usuario: int | None = Field(
        None,
        gt=0,
        description="ID del nuevo usuario asignado"
    )


class AsignacionResponse(AsignacionBase):
    """Schema de respuesta con ID y fecha"""
    id_asignacion: int = Field(
        ...,
        description="ID único de la asignación"
    )
    fecha_asignacion: datetime = Field(
        ...,
        description="Fecha y hora de la asignación"
    )
    
    model_config = {
        "from_attributes": True
    }
