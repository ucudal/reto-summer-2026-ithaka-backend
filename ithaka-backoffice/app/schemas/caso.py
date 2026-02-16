"""
Schemas CASO
------------
Define casos de emprendedores (postulaciones/proyectos).
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any


class CasoBase(BaseModel):
    """Campos comunes de caso"""
    nombre_caso: str = Field(
        ...,
        max_length=200,
        description="Nombre del caso/proyecto",
        examples=["App de delivery sustentable"]
    )
    
    descripcion: Optional[str] = Field(
        None,
        description="Descripción detallada del caso"
    )
    
    datos_chatbot: Optional[dict[str, Any]] = Field(
        None,
        description="Datos capturados por el chatbot en formato JSON"
    )
    
    consentimiento_datos: bool = Field(
        False,
        description="Indica si el emprendedor dio consentimiento para usar sus datos"
    )
    
    id_emprendedor: int = Field(
        ...,
        description="ID del emprendedor que presenta el caso"
    )
    
    id_convocatoria: Optional[int] = Field(
        None,
        description="ID de la convocatoria asociada"
    )
    
    id_estado: int = Field(
        ...,
        description="ID del estado actual del caso"
    )


class CasoCreate(CasoBase):
    """Schema para crear caso (POST)"""
    pass


class CasoUpdate(BaseModel):
    """Schema para actualizar caso (PUT)"""
    nombre_caso: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    datos_chatbot: Optional[dict[str, Any]] = None
    consentimiento_datos: Optional[bool] = None
    id_emprendedor: Optional[int] = None
    id_convocatoria: Optional[int] = None
    id_estado: Optional[int] = None


class CasoResponse(CasoBase):
    """Schema para respuesta (GET)"""
    id_caso: int = Field(..., description="ID único del caso")
    fecha_creacion: datetime = Field(..., description="Fecha de creación del caso")
    
    class Config:
        from_attributes = True
