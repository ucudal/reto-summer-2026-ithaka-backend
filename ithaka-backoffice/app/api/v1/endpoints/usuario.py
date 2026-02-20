"""
Modelo USUARIO
--------------
TODO: Implementar usando TEMPLATE.py como guía

Tabla: usuario
Columnas según SQL:
- id_usuario SERIAL PRIMARY KEY
- nombre VARCHAR(150) NOT NULL
- email VARCHAR(150) NOT NULL UNIQUE
- password_hash TEXT NOT NULL
- activo BOOLEAN DEFAULT TRUE
- id_rol INTEGER NOT NULL (FK a rol)
"""

# from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.database import Base
# 
# class Usuario(Base):
#     __tablename__ = "usuario"
#     # ... agregar columnas

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.core.security import hash_password, get_current_user, require_role

router = APIRouter()


# ============================================================================
# LISTAR USUARIOS (GET /)
# ============================================================================
@router.get("/", status_code=status.HTTP_200_OK)
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(require_role(["admin"]))  # TEMPORALMENTE DESACTIVADO - JWT
):
    """Listar todos los usuarios activos (solo admin)"""
    usuarios = db.query(Usuario).filter(
        Usuario.activo == True
    ).offset(skip).limit(limit).all()
    return usuarios

# ============================================================================
# OBTENER USUARIO (GET /{id})
# ============================================================================
@router.get("/{usuario_id}", status_code=status.HTTP_200_OK)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(get_current_user)  # TEMPORALMENTE DESACTIVADO - JWT
):
    """Obtener un usuario por ID (propio perfil o admin)"""
    # Verificar permisos: solo puede ver su propio perfil o ser admin
    # if current_user.id_usuario != usuario_id and current_user.rol.nombre_rol != "admin":  # TEMPORALMENTE DESACTIVADO - JWT
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="No tienes permisos para ver este usuario"
    #     )
    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return usuario

# ============================================================================
# CREAR USUARIO (POST /)
# ============================================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(
    nombre: str,
    apellido: str,
    email: str,
    password: str,
    id_rol: int,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(require_role(["admin"]))  # TEMPORALMENTE DESACTIVADO - JWT
):
    """Crear nuevo usuario (solo admin)"""
    # Verificar que el rol existe
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol inválido"
        )
    
    # Verificar que el email no exista
    usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )
    
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        password_hash=hash_password(password),
        id_rol=id_rol,
        activo=True
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario

# ============================================================================
# ACTUALIZAR USUARIO (PUT /{id})
# ============================================================================
@router.put("/{usuario_id}", status_code=status.HTTP_200_OK)
def actualizar_usuario(
    usuario_id: int,
    nombre: str = None,
    apellido: str = None,
    email: str = None,
    password: str = None,
    id_rol: int = None,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(get_current_user)  # TEMPORALMENTE DESACTIVADO - JWT
):
    """Actualizar usuario (propio perfil o admin)"""
    # Verificar permisos
    # if current_user.id_usuario != usuario_id and current_user.rol.nombre_rol != "admin":  # TEMPORALMENTE DESACTIVADO - JWT
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="No tienes permisos para actualizar este usuario"
    #     )
    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar campos
    if nombre:
        usuario.nombre = nombre
    if apellido:
        usuario.apellido = apellido
    if email:
        # Verificar que el email no esté en uso
        email_existente = db.query(Usuario).filter(
            Usuario.email == email,
            Usuario.id_usuario != usuario_id
        ).first()
        if email_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya está en uso"
            )
        usuario.email = email
    if password:
        usuario.password_hash = hash_password(password)
    if id_rol:
        # Solo admin puede cambiar roles
        # if current_user.rol.nombre_rol != "admin":  # TEMPORALMENTE DESACTIVADO - JWT
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Solo admin puede cambiar roles"
        #     )
        rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rol inválido"
            )
        usuario.id_rol = id_rol
    
    db.commit()
    db.refresh(usuario)
    return usuario     

# ============================================================================
# DESACTIVAR USUARIO (DELETE /{id}) - Soft delete
# ============================================================================
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(require_role(["admin"]))  # TEMPORALMENTE DESACTIVADO - JWT
):
    """Desactivar usuario (solo admin)"""
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir desactivarse a sí mismo
    # if usuario.id_usuario == current_user.id_usuario:  # TEMPORALMENTE DESACTIVADO - JWT
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="No puedes desactivar tu propio usuario"
    #     )
    
    usuario.activo = False
    db.commit()
    
    return None