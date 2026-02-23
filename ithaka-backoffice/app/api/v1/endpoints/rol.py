"""
Endpoints ROL
-------------
Gestión de roles de usuario en el sistema.

Endpoints:
- GET /api/v1/roles - Listar todos
- GET /api/v1/roles/{id} - Obtener uno
- POST /api/v1/roles - Crear
- PUT /api/v1/roles/{id} - Actualizar
- DELETE /api/v1/roles/{id} - Eliminar
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import require_role
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.services.auditoria_service import registrar_auditoria_general

router = APIRouter()


@router.get("/", response_model=list[RolResponse])
def listar_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """Listar todos los roles del sistema (Solo Admin)"""
    roles = db.query(Rol).offset(skip).limit(limit).all()
    return roles


@router.get("/{rol_id}", response_model=RolResponse)
def obtener_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """Obtener un rol específico por ID (Solo Admin)"""
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con ID {rol_id} no encontrado"
        )
    
    return rol


@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def crear_rol(
    rol_data: RolCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Crear un nuevo rol (Solo Admin)
    
    El nombre del rol debe ser único.
    """
    # Verificar si ya existe un rol con ese nombre
    rol_existente = db.query(Rol).filter(Rol.nombre_rol == rol_data.nombre_rol).first()
    if rol_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un rol con el nombre '{rol_data.nombre_rol}'"
        )
    
    nuevo_rol = Rol(**rol_data.model_dump())
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    
    # Registrar en auditoría
    registrar_auditoria_general(
        db=db,
        id_usuario=current_user.id_usuario,
        accion=f"Creó el rol '{nuevo_rol.nombre_rol}'",
        valor_nuevo=nuevo_rol.nombre_rol
    )
    
    return nuevo_rol


@router.put("/{rol_id}", response_model=RolResponse)
def actualizar_rol(
    rol_id: int,
    rol_data: RolUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """Actualizar un rol existente (Solo Admin)"""
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con ID {rol_id} no encontrado"
        )
    
    # Si se actualiza el nombre, verificar que no exista otro rol con ese nombre
    if rol_data.nombre_rol and rol_data.nombre_rol != rol.nombre_rol:
        rol_existente = db.query(Rol).filter(Rol.nombre_rol == rol_data.nombre_rol).first()
        if rol_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un rol con el nombre '{rol_data.nombre_rol}'"
            )
    
    update_data = rol_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rol, field, value)
    
    db.commit()
    db.refresh(rol)
    
    # Registrar en auditoría
    registrar_auditoria_general(
        db=db,
        id_usuario=current_user.id_usuario,
        accion=f"Actualizó el rol '{rol.nombre_rol}'",
        valor_nuevo=update_data
    )
    
    return rol


@router.delete("/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Eliminar un rol (Solo Admin)
    
    ADVERTENCIA: Solo se puede eliminar si no hay usuarios asignados a este rol.
    """
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con ID {rol_id} no encontrado"
        )
    
    # Verificar si hay usuarios con este rol
    from app.models.usuario import Usuario
    usuarios_con_rol = db.query(Usuario).filter(Usuario.id_rol == rol_id).count()
    
    if usuarios_con_rol > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar el rol. Hay {usuarios_con_rol} usuario(s) asignado(s) a este rol."
        )
    
    # Registrar en auditoría antes de eliminar
    registrar_auditoria_general(
        db=db,
        id_usuario=current_user.id_usuario,
        accion=f"Eliminó el rol '{rol.nombre_rol}'",
        valor_anterior=rol.nombre_rol
    )
    
    db.delete(rol)
    db.commit()
    
    return None
