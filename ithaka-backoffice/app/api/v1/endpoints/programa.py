"""
Endpoints PROGRAMA
------------------
TODO: Implementar usando TEMPLATE.py como guía

Endpoints a crear:
- GET /api/v1/programas - Listar todos
- GET /api/v1/programas/{id} - Obtener uno
- POST /api/v1/programas - Crear
- PUT /api/v1/programas/{id} - Actualizar
- DELETE /api/v1/programas/{id} - Eliminar
"""

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.api.deps import get_db
# from app.models.programa import Programa
# from app.schemas.programa import ProgramaCreate, ProgramaUpdate, ProgramaResponse
# 
# router = APIRouter()
# 
# @router.get("/")
# def listar_programas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     # ... implementar
#     pass
