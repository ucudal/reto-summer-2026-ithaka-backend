"""
Endpoints ROL
-------------
Gestión de roles del sistema.

Permisos:
- GET /roles        → Admin o Tutor (consulta)
- GET /roles/{id}   → Admin o Tutor
- POST /roles       → Solo Admin
- PUT /roles/{id}   → Solo Admin
- DELETE /roles/{id}→ Solo Admin
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_admin, require_admin_o_tutor
from app.models.rol import Rol
from app.models.usuario import Usuario

router = APIRouter()


@router.get("/")
def listar_roles(
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(require_admin_o_tutor)
):
    return db.query(Rol).all()


@router.get("/{id_rol}")
def obtener_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(require_admin_o_tutor)
):
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.post("/", status_code=201)
def crear_rol(
    nombre_rol: str,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(require_admin)  
):
    if db.query(Rol).filter(Rol.nombre_rol == nombre_rol).first():
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")

    nuevo = Rol(nombre_rol=nombre_rol)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Rol creado correctamente", "id_rol": nuevo.id_rol}


@router.put("/{id_rol}")
def actualizar_rol(
    id_rol: int,
    nombre_rol: str,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(require_admin) 
):
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    if db.query(Rol).filter(Rol.nombre_rol == nombre_rol, Rol.id_rol != id_rol).first():
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")

    rol.nombre_rol = nombre_rol
    db.commit()
    db.refresh(rol)
    return {"mensaje": "Rol actualizado correctamente"}


@router.delete("/{id_rol}")
def eliminar_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    _usuario: Usuario = Depends(require_admin)  
):
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    if rol.usuarios:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar: {len(rol.usuarios)} usuario(s) tienen este rol"
        )

    db.delete(rol)
    db.commit()
    return {"mensaje": "Rol eliminado correctamente"}