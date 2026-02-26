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
from typing import List

from app.api.deps import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioResponse, UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password, get_current_user, require_role

router = APIRouter()


# ============================================================================
# LISTAR USUARIOS (GET /)
# ============================================================================
@router.get("/", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    """
    Listar todos los usuarios (activos e inactivos)
    """

    usuarios = db.query(Usuario)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return usuarios

# ============================================================================
# OBTENER USUARIO (GET /{id})
# ============================================================================
@router.get("/{usuario_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    # Si es Tutor, solo puede ver su propio perfil
    if current_user.rol.nombre_rol == "Tutor" and current_user.id_usuario != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este usuario"
        )
    
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
@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Crear nuevo usuario
    
    Permisos:
    - Admin: Puede crear usuarios
    - Coordinador: NO puede crear usuarios
    - Tutor: NO puede crear usuarios
    """
    # Verificar que el rol existe
    rol = db.query(Rol).filter(Rol.id_rol == usuario_data.id_rol).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol inválido"
        )
    
    # Verificar que el email no exista
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )
    
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        apellido=usuario_data.apellido,
        email=usuario_data.email,
        password_hash=hash_password(usuario_data.password),
        id_rol=usuario_data.id_rol,
        activo=True
    )
    
    db.add(nuevo_usuario)
    db.flush()  # Obtener id antes del commit
    
    # Auditoría: Usuario creado
    from app.services.auditoria_service import registrar_auditoria_general
    registrar_auditoria_general(
        db=db,
        accion="Usuario creado",
        id_usuario=current_user.id_usuario,
        valor_nuevo=f"Usuario '{nuevo_usuario.nombre} {nuevo_usuario.apellido or ''}' creado (email={nuevo_usuario.email}, rol={rol.nombre_rol})"
    )
    
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario

# ============================================================================
# ACTUALIZAR USUARIO (PUT /{id})
# ============================================================================
@router.put("/{usuario_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """
    Actualizar usuario
    
    Permisos:
    - Admin: Puede actualizar cualquier usuario
    - Coordinador: Solo puede actualizar su propio perfil
    - Tutor: Solo puede actualizar su propio perfil
    """
    # Si no es Admin, solo puede actualizar su propio perfil
    if current_user.rol.nombre_rol != "Admin" and current_user.id_usuario != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este usuario"
        )
    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar campos
    if usuario_data.nombre:
        usuario.nombre = usuario_data.nombre
    if usuario_data.apellido:
        usuario.apellido = usuario_data.apellido
    if usuario_data.email:
        # Verificar que el email no esté en uso
        email_existente = db.query(Usuario).filter(
            Usuario.email == usuario_data.email,
            Usuario.id_usuario != usuario_id
        ).first()
        if email_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya está en uso"
            )
        usuario.email = usuario_data.email
    if usuario_data.password:
        usuario.password_hash = hash_password(usuario_data.password)
    if usuario_data.activo is not None:
        usuario.activo = usuario_data.activo
    if usuario_data.id_rol:
        # Solo admin puede cambiar roles
        if current_user.rol.nombre_rol != "Admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo admin puede cambiar roles"
            )
        rol = db.query(Rol).filter(Rol.id_rol == usuario_data.id_rol).first()
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rol inválido"
            )
        usuario.id_rol = usuario_data.id_rol
    
    db.commit()
    db.refresh(usuario)
    return usuario     

# ============================================================================
# DESACTIVAR USUARIO (DELETE /{id}) - Soft delete con auditoría
# ============================================================================
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Desactivar usuario (soft delete)
    
    Permisos:
    - Admin: Puede desactivar usuarios
    - Coordinador: NO puede desactivar usuarios
    - Tutor: NO puede desactivar usuarios
    
    Los usuarios NO se eliminan físicamente para preservar el historial
    de auditorías, asignaciones y notas. En su lugar, se marcan como inactivos.
    """
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir desactivarse a sí mismo
    if usuario.id_usuario == current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propio usuario"
        )
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya está inactivo"
        )
    
    # Auditoría: Usuario desactivado
    from app.services.auditoria_service import registrar_auditoria_general
    registrar_auditoria_general(
        db=db,
        accion="Usuario desactivado",
        id_usuario=current_user.id_usuario,
        valor_anterior=f"Usuario '{usuario.nombre} {usuario.apellido or ''}' (activo=True)",
        valor_nuevo=f"Usuario '{usuario.nombre} {usuario.apellido or ''}' (activo=False)"
    )
    
    usuario.activo = False
    db.commit()
    
    return None


# ============================================================================
# REACTIVAR USUARIO (PUT /{id}/reactivar)
# ============================================================================
@router.put("/{usuario_id}/reactivar", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def reactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Reactivar usuario previamente desactivado
    
    Permisos:
    - Admin: Puede reactivar usuarios
    - Coordinador: NO puede reactivar usuarios
    - Tutor: NO puede reactivar usuarios
    """
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya está activo"
        )
    
    # Auditoría: Usuario reactivado
    from app.services.auditoria_service import registrar_auditoria_general
    registrar_auditoria_general(
        db=db,
        accion="Usuario reactivado",
        id_usuario=current_user.id_usuario,
        valor_anterior=f"Usuario '{usuario.nombre} {usuario.apellido or ''}' (activo=False)",
        valor_nuevo=f"Usuario '{usuario.nombre} {usuario.apellido or ''}' (activo=True)"
    )
    
    usuario.activo = True
    db.commit()
    db.refresh(usuario)
    
    return usuario