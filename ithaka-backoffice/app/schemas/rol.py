"""
Schemas ROL
-----------
Validaciones para roles de usuario.
"""

from pydantic import BaseModel, Field
from typing import Optional


class RolBase(BaseModel):
    """Campos comunes de rol"""
    nombre_rol: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre del rol",
        examples=["Admin", "Coordinador", "Tutor"]
    )


class RolCreate(RolBase):
    """Schema para crear rol"""
    pass


class RolUpdate(BaseModel):
    """Schema para actualizar rol"""
    nombre_rol: Optional[str] = Field(None, min_length=1, max_length=50)


class RolResponse(RolBase):
    """Schema para respuesta"""
    id_rol: int
    
    class Config:
        from_attributes = True
