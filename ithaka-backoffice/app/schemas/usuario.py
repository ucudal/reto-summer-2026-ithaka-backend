"""
Schemas USUARIO
---------------
TODO: Implementar usando TEMPLATE.py como guía

Campos según SQL:
- id_usuario (solo en Response)
- nombre
- email
- password_hash (cuidado: no exponerlo en Response)
- activo
- id_rol
"""

# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional
# 
# class UsuarioBase(BaseModel):
#     # ... campos comunes
#     pass
# 
# class UsuarioCreate(UsuarioBase):
#     # password sin hashear
#     pass
# 
# class UsuarioUpdate(BaseModel):
#     # ... campos opcionales
#     pass
# 
# class UsuarioResponse(UsuarioBase):
#     id_usuario: int
#     # NO incluir password_hash en Response
#     class Config:
#         from_attributes = True
