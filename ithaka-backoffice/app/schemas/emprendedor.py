from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class EmprendedorBase(BaseModel):
    nombre: str = Field(
        ...,  
        min_length=1,
        max_length=150,
        description="Nombre del emprendedor",
        examples=["Juan"]
    )
    
    apellido: str = Field(
        ...,  
        min_length=1,
        max_length=150,
        description="Apellido del emprendedor",
        examples=["Pérez"]
    )
    
    email: EmailStr = Field(
        ..., 
        max_length=150,
        description="Email del emprendedor",
        examples=["juan.perez@example.com"]
    )
    
    telefono: Optional[str] = Field(
        None,  
        max_length=50,
        description="Teléfono de contacto",
        examples=["+598 99 123 456"]
    )
    
    documento_identidad: Optional[str] = Field(
        None,
        max_length=50,
        description="Documento de identidad (CI, DNI, pasaporte)",
        examples=["12345678"]
    )
    
    pais_residencia: Optional[str] = Field(
        None,
        max_length=100,
        description="País de residencia",
        examples=["Uruguay"]
    )
    
    ciudad_residencia: Optional[str] = Field(
        None,
        max_length=100,
        description="Ciudad de residencia",
        examples=["Montevideo"]
    )
    
    campus_ucu: Optional[str] = Field(
        None,
        max_length=100,
        description="Campus de la UCU",
        examples=["Campus Montevideo", "Campus Salto"]
    )
    
    relacion_ucu: Optional[str] = Field(
        None,
        max_length=100,
        description="Relación con la UCU",
        examples=["Estudiante", "Egresado", "Externo"]
    )
    
    facultad_ucu: Optional[str] = Field(
        None,
        max_length=100,
        description="Facultad en la UCU",
        examples=["Ingeniería", "Empresariales", "Comunicación"]
    )
    
    canal_llegada: Optional[str] = Field(
        None,
        max_length=100,
        description="Canal por el cual llegó a Ithaka",
        examples=["Web", "Referido", "ChatBot", "LinkedIn"]
    )
    
    motivacion: Optional[str] = Field(
        None,
        description="Motivación para emprender",
        examples=["Quiero desarrollar mi startup tecnológica"]
    )


class EmprendedorCreate(EmprendedorBase):
    pass  # Hereda todos los campos de EmprendedorBase


class EmprendedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    apellido: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=150)
    telefono: Optional[str] = Field(None, max_length=50)
    documento_identidad: Optional[str] = Field(None, max_length=50)
    pais_residencia: Optional[str] = Field(None, max_length=100)
    ciudad_residencia: Optional[str] = Field(None, max_length=100)
    campus_ucu: Optional[str] = Field(None, max_length=100)
    relacion_ucu: Optional[str] = Field(None, max_length=100)
    facultad_ucu: Optional[str] = Field(None, max_length=100)
    canal_llegada: Optional[str] = Field(None, max_length=100)
    motivacion: Optional[str] = None



class EmprendedorResponse(EmprendedorBase):
    id_emprendedor: int = Field(
        ...,
        description="ID único del emprendedor",
        examples=[1]
    )
    
    fecha_registro: datetime = Field(
        ...,
        description="Fecha y hora de registro en el sistema"
    )
    
    class Config:
        from_attributes = True



class EmprendedorListResponse(BaseModel):
    total: int = Field(
        ...,
        description="Cantidad total de emprendedores",
        examples=[25]
    )
    
    emprendedores: list[EmprendedorResponse] = Field(
        ...,
        description="Lista de emprendedores"
    )


