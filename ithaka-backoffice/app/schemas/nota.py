"""
Schemas NOTA
------------
TODO: Implementar usando TEMPLATE.py como guía

Campos según SQL:
- id_nota (solo en Response)
- contenido
- fecha (autogenerado)
- id_usuario
- id_caso
"""

# from pydantic import BaseModel, Field
# from datetime import datetime
# from typing import Optional
# 
# class NotaBase(BaseModel):
#     # ... campos comunes
#     pass
# 
# class NotaCreate(NotaBase):
#     pass
# 
# class NotaUpdate(BaseModel):
#     # ... campos opcionales
#     pass
# 
# class NotaResponse(NotaBase):
#     id_nota: int
#     fecha: datetime
#     class Config:
#         from_attributes = True
