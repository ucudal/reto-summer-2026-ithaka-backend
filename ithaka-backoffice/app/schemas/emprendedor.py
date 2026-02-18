from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class EmprendedorBase(BaseModel):
    nombre: str = Field(
        ...,  
        min_length=1,
        max_length=150,
        description="Nombre completo del emprendedor",
        examples=["Juan Pérez"]
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
    
    vinculo_institucional: Optional[str] = Field(
        None,
        max_length=150,
        description="Relación con la institución",
        examples=["Estudiante UCU", "Egresado", "Externo"]
    )



class EmprendedorCreate(EmprendedorBase):
    pass  # Hereda todos los campos de EmprendedorBase


class EmprendedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=150)
    telefono: Optional[str] = Field(None, max_length=50)
    vinculo_institucional: Optional[str] = Field(None, max_length=150)



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


