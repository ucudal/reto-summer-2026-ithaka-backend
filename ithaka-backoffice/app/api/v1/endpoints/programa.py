from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.programa import Programa
from app.models.usuario import Usuario
from app.schemas.programa import ProgramaCreate, ProgramaUpdate, ProgramaResponse
from app.core.security import require_role

router = APIRouter()


@router.get("/", response_model=List[ProgramaResponse])
def listar_programas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """Listar programas (todos los roles)"""
    return db.query(Programa).offset(skip).limit(limit).all()


@router.get("/{programa_id}", response_model=ProgramaResponse)
def obtener_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """Obtener programa (todos los roles)"""
    programa = db.query(Programa).filter(Programa.id_programa == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa


@router.post("/", response_model=ProgramaResponse, status_code=status.HTTP_201_CREATED)
def crear_programa(
    programa_data: ProgramaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    """Crear programa (Admin y Coordinador)"""
    nuevo = Programa(**programa_data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{programa_id}", response_model=ProgramaResponse)
def actualizar_programa(
    programa_id: int,
    programa_data: ProgramaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    """Actualizar programa (Admin y Coordinador)"""
    programa = db.query(Programa).filter(Programa.id_programa == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    update_data = programa_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(programa, field, value)

    db.commit()
    db.refresh(programa)
    return programa


@router.delete("/{programa_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """Eliminar programa (Solo Admin)"""
    programa = db.query(Programa).filter(Programa.id_programa == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    db.delete(programa)
    db.commit()
    return None