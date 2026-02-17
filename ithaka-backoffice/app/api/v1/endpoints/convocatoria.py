"""
Endpoints CONVOCATORIA
----------------------
TODO: Implementar usando TEMPLATE.py como guía

Endpoints a crear:
- GET /api/v1/convocatorias - Listar todas
- GET /api/v1/convocatorias/{id} - Obtener una
- POST /api/v1/convocatorias - Crear
- PUT /api/v1/convocatorias/{id} - Actualizar
- DELETE /api/v1/convocatorias/{id} - Eliminar
"""

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.api.deps import get_db
# from app.models.convocatoria import Convocatoria
# from app.schemas.convocatoria import ConvocatoriaCreate, ConvocatoriaUpdate, ConvocatoriaResponse
# 
# router = APIRouter()
# 
# @router.get("/")
# def listar_convocatorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     # ... implementar
#     pass
