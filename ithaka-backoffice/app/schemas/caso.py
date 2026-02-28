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
        gt=0,
        description="ID del emprendedor que presenta el caso",
        examples=[1]
    )
    
    id_convocatoria: Optional[int] = Field(
        None,
        gt=0,
        description="ID de la convocatoria asociada",
        examples=[1]
    )
    
    id_estado: int = Field(
        ...,
        gt=0,
        description="ID del estado actual del caso",
        examples=[1]
    )


class CasoCreate(BaseModel):
    """Schema para crear caso (POST). El backend asigna estado Postulado automáticamente."""
    nombre_caso: str = Field(
        ...,
        max_length=200,
        description="Nombre del caso/proyecto",
        examples=["EcoApp - Reciclaje Inteligente"]
    )
    descripcion: Optional[str] = Field(
        None,
        description="Descripción detallada del caso",
        examples=["Aplicación móvil para facilitar el reciclaje urbano mediante gamificación"]
    )
    datos_chatbot: Optional[dict[str, Any]] = Field(
        None,
        description="Datos capturados por el chatbot en formato JSON",
        examples=[{"sector": "Tecnología", "modelo": "B2C", "estado_producto": "MVP en desarrollo"}]
    )
    id_emprendedor: int = Field(
        ...,
        gt=0,
        description="ID del emprendedor que presenta el caso",
        examples=[1]
    )
    id_convocatoria: Optional[int] = Field(
        None,
        gt=0,
        description="ID de la convocatoria asociada",
        examples=[1]
    )


class CasoUpdate(BaseModel):
    """Schema para actualizar caso (PUT)"""
    nombre_caso: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    datos_chatbot: Optional[dict[str, Any]] = None
    id_emprendedor: Optional[int] = Field(None, gt=0, examples=[1])
    id_convocatoria: Optional[int] = Field(None, gt=0, examples=[1])
    id_estado: Optional[int] = Field(None, gt=0, examples=[2])


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
