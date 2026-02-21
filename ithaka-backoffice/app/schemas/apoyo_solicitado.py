"""
Schemas APOYO_SOLICITADO
------------------------
Validación de datos para categorías de apoyo solicitadas.
"""

from pydantic import BaseModel, Field


class ApoyoSolicitadoBase(BaseModel):
    """Campos comunes de apoyo solicitado"""
    categoria_apoyo: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Categoría de apoyo solicitada",
        examples=["Mentoría técnica", "Financiamiento", "Asesoría legal"]
    )
    id_caso: int = Field(
        ...,
        gt=0,
        description="ID del caso que solicita el apoyo",
        examples=[1]
    )


class ApoyoSolicitadoCreate(ApoyoSolicitadoBase):
    """Schema para crear apoyo solicitado"""
    pass


class ApoyoSolicitadoUpdate(BaseModel):
    """Schema para actualizar apoyo solicitado"""
    categoria_apoyo: str | None = Field(
        None,
        min_length=1,
        max_length=150,
        description="Categoría de apoyo solicitada"
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
