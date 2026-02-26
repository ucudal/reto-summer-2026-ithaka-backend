from pydantic import BaseModel, Field
from typing import Optional, Literal


class CatalogoApoyosBase(BaseModel):
    nombre: str = Field(
        ...,
        max_length=100,
        description="Nombre del apoyo",
        examples=["Mentoría", "Financiamiento", "Networking"]
    )


class CatalogoApoyosCreate(CatalogoApoyosBase):
    pass


class CatalogoApoyosUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)


class CatalogoApoyosResponse(CatalogoApoyosBase):
    id_catalogo_apoyo: int = Field(..., description="ID único del catálogo de apoyos")
    
    class Config:
        from_attributes = True
