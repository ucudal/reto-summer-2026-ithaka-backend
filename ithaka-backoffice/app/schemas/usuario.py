"""
Schemas USUARIO
---------------
Validaciones para usuarios del sistema.

IMPORTANTE: No exponer password_hash en Response.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UsuarioBase(BaseModel):
    """Campos comunes de usuario"""
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Nombre del usuario",
        examples=["Juan"]
    )
    
    apellido: Optional[str] = Field(
        None,
        max_length=150,
        description="Apellido del usuario",
        examples=["Pérez"]
    )
    
    email: EmailStr = Field(
        ...,
        max_length=150,
        description="Email del usuario (debe ser válido)",
        examples=["juan.perez@ithaka.com"]
    )
    
    activo: bool = Field(
        True,
        description="Indica si el usuario está activo"
    )
    
    id_rol: int = Field(
        ...,
        description="ID del rol asignado al usuario",
        examples=[1, 2, 3]
    )


class UsuarioCreate(UsuarioBase):
    """Schema para crear un usuario (incluye password sin hashear)"""
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password del usuario (mínimo 8 caracteres)",
        examples=["password123"]
    )


class UsuarioUpdate(BaseModel):
    """Schema para actualizar usuario"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    apellido: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=150)
    activo: Optional[bool] = None
    id_rol: Optional[int] = None  
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UsuarioResponse(BaseModel):
    """Schema para respuesta (NO incluye password_hash)"""
    id_usuario: int
    nombre: str
    apellido: Optional[str]
    email: str
    activo: bool
    id_rol: int
    
    class Config:
        from_attributes = True
