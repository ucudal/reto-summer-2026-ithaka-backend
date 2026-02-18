from pydantic import BaseModel, Field
from typing import Optional


class ProgramaBase(BaseModel):
    nombre: str = Field(..., max_length=150, description="Nombre del programa")
    activo: bool = Field(True, description="Indica si el programa está activo")


class ProgramaCreate(ProgramaBase):
    pass


class ProgramaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    activo: Optional[bool] = None


class ProgramaResponse(ProgramaBase):
    id_programa: int = Field(..., description="ID único del programa")

    class Config:
        from_attributes = True
