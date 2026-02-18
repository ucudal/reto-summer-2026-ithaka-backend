"""
Endpoints USUARIO
-----------------
TODO: Implementar usando TEMPLATE.py como guía

Endpoints a crear:
- GET /api/v1/usuarios - Listar todos
- GET /api/v1/usuarios/{id} - Obtener uno
- POST /api/v1/usuarios - Crear (hashear password)
- PUT /api/v1/usuarios/{id} - Actualizar
- DELETE /api/v1/usuarios/{id} - Eliminar

IMPORTANTE: Hashear el password antes de guardarlo
"""

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.api.deps import get_db
# from app.models.usuario import Usuario
# from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
# 
# router = APIRouter()
# 
# @router.post("/", status_code=status.HTTP_201_CREATED)
# def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
#     # TODO: Hashear password antes de guardar
#     # from passlib.context import CryptContext
#     # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     # password_hash = pwd_context.hash(usuario_data.password)
#     pass
