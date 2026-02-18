from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ConvocatoriaBase(BaseModel):
    nombre: str = Field(..., max_length=150, description="Nombre de la convocatoria")
    fecha_cierre: Optional[datetime] = Field(None, description="Fecha/hora de cierre")


class ConvocatoriaCreate(ConvocatoriaBase):
    pass


class ConvocatoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    fecha_cierre: Optional[datetime] = None


class ConvocatoriaResponse(ConvocatoriaBase):
    id_convocatoria: int = Field(..., description="ID único de la convocatoria")

    class Config:
        from_attributes = True