from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal


class CatalogoEstadosBase(BaseModel):
    nombre_estado: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del estado",
        examples=["En Revisión", "Aprobado", "Rechazado"]
    )
    
    tipo_caso: Literal["postulacion", "proyecto"] = Field(
        ...,
        description="Tipo de caso al que aplica este estado (en minúsculas)"
    )


class CatalogoEstadosCreate(CatalogoEstadosBase):
    @field_validator('nombre_estado')
    @classmethod
    def validate_nombre_not_blank(cls, v: str) -> str:
        """Validar que nombre_estado no sea solo espacios en blanco"""
        if not v or not v.strip():
            raise ValueError('nombre_estado no puede estar vacío o contener solo espacios')
        return v.strip()


class CatalogoEstadosUpdate(BaseModel):
    nombre_estado: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_caso: Optional[Literal["Postulacion", "Proyecto"]] = None


class CatalogoEstadosResponse(CatalogoEstadosBase):
    id_estado: int = Field(..., description="ID único del estado")
    
    class Config:
        from_attributes = True
