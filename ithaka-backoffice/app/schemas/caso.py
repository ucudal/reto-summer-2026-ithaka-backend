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
    """Schema para crear caso (POST). El backend asigna estado Postulado automáticamente."""
    id_estado: Optional[int] = Field(
        None,
        description="Ignorado en creación: el backend siempre asigna el estado Postulado"
    )


class CasoUpdate(BaseModel):
    """Schema para actualizar caso (PUT)"""
    nombre_caso: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    datos_chatbot: Optional[dict[str, Any]] = None
    id_emprendedor: Optional[int] = None
    id_convocatoria: Optional[int] = None
    id_estado: Optional[int] = None


class CasoResponse(CasoBase):
    """Schema para respuesta (GET)"""
    id_caso: int = Field(..., description="ID único del caso")
    fecha_creacion: datetime = Field(..., description="Fecha de creación del caso")
    nombre_estado: Optional[str] = Field(None, description="Nombre del estado actual")
    tipo_caso: Optional[str] = Field(None, description="Tipo de caso")
    emprendedor: Optional[str] = Field(None, description="Nombre completo del emprendedor")
    convocatoria: Optional[str] = Field(None, description="Nombre de la convocatoria")
    tutor_nombre: Optional[str] = Field(None, description="Nombre completo del tutor")
    id_tutor: Optional[Any] = Field(None, description="ID del tutor o 'Sin Asignar'")
    asignacion: Optional[Any] = Field(None, description="ID de la asignación o 'Sin Asignar'")
    
    class Config:
        from_attributes = True
