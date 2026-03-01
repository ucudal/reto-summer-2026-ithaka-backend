"""
Schemas APOYO_SOLICITADO
------------------------
Validación de datos para categorías de apoyo solicitadas.
"""

from pydantic import BaseModel, Field


class ApoyoSolicitadoBase(BaseModel):
    """Campos comunes de apoyo solicitado"""
    id_catalogo_apoyo: int = Field(
        ...,
        gt=0,
        description="ID del catálogo de apoyo solicitado",
        examples=[1, 2, 3]
    )
    id_caso: int = Field(
        ...,
        gt=0,
        description="ID del caso que solicita el apoyo",
        examples=[1]
    )


class ApoyoSolicitadoCreate(ApoyoSolicitadoBase):
    """Schema para crear apoyo solicitado"""
    class Config:
        json_schema_extra = {
            "example": {
                "id_catalogo_apoyo": 1,
                "id_caso": 1
            }
        }


class ApoyoSolicitadoUpdate(BaseModel):
    """Schema para actualizar apoyo solicitado"""
    id_catalogo_apoyo: int | None = Field(
        None,
        gt=0,
        description="ID del catálogo de apoyo solicitado"
    )


class ApoyoSolicitadoResponse(ApoyoSolicitadoBase):
    """Schema de respuesta con ID"""
    id_apoyo_solicitado: int = Field(
        ...,
        description="ID único del apoyo solicitado"
    )
    
    model_config = {
        "from_attributes": True
    }
