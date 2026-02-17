"""
Schemas APOYO
-------------
TODO: Implementar usando TEMPLATE.py como guía

Campos según SQL:
- id_apoyo (solo en Response)
- tipo_apoyo
- fecha_inicio
- fecha_fin
- id_caso
- id_programa
"""

# from pydantic import BaseModel, Field
# from datetime import date
# from typing import Optional
# 
# class ApoyoBase(BaseModel):
#     # ... campos comunes
#     pass
# 
# class ApoyoCreate(ApoyoBase):
#     pass
# 
# class ApoyoUpdate(BaseModel):
#     # ... campos opcionales
#     pass
# 
# class ApoyoResponse(ApoyoBase):
#     id_apoyo: int
#     class Config:
#         from_attributes = True
