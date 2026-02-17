"""
Schemas AUDITORIA
-----------------
TODO: Implementar usando TEMPLATE.py como guía

Campos según SQL:
- id_auditoria (solo en Response)
- timestamp (autogenerado)
- accion
- valor_anterior
- valor_nuevo
- id_usuario
- id_caso
"""

# from pydantic import BaseModel, Field
# from datetime import datetime
# from typing import Optional
# 
# class AuditoriaBase(BaseModel):
#     # ... campos comunes
#     pass
# 
# class AuditoriaCreate(AuditoriaBase):
#     pass
# 
# class AuditoriaUpdate(BaseModel):
#     # ... campos opcionales
#     pass
# 
# class AuditoriaResponse(AuditoriaBase):
#     id_auditoria: int
#     timestamp: datetime
#     class Config:
#         from_attributes = True
