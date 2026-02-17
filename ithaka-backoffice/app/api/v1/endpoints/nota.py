"""
Endpoints NOTA
--------------
TODO: Implementar usando TEMPLATE.py como guía

Endpoints a crear:
- GET /api/v1/notas - Listar todas
- GET /api/v1/notas/{id} - Obtener una
- POST /api/v1/notas - Crear
- PUT /api/v1/notas/{id} - Actualizar
- DELETE /api/v1/notas/{id} - Eliminar
"""

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.api.deps import get_db
# from app.models.nota import Nota
# from app.schemas.nota import NotaCreate, NotaUpdate, NotaResponse
# 
# router = APIRouter()
# 
# @router.get("/")
# def listar_notas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     # ... implementar
#     pass
