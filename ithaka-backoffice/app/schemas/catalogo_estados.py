from pydantic import BaseModel, Field
from typing import Optional, Literal


class CatalogoEstadosBase(BaseModel):
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
    pass


class CatalogoEstadosUpdate(BaseModel):
    nombre_estado: Optional[str] = Field(None, max_length=100)
    tipo_caso: Optional[Literal["Postulacion", "Proyecto"]] = None


class CatalogoEstadosResponse(CatalogoEstadosBase):
    id_estado: int = Field(..., description="ID único del estado")
    
    class Config:
        from_attributes = True
