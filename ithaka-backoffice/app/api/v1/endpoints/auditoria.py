"""
Endpoints AUDITORIA
-------------------
Registro de eventos para trazabilidad del sistema.

Endpoints expuestos:
- GET /api/v1/auditoria - Listar registros (con filtros)
- GET /api/v1/auditoria/{id} - Obtener un registro
- GET /api/v1/auditoria/staff/{id_usuario} - Acciones de un miembro del staff

NOTA: Los registros de auditoría son de solo lectura en API pública.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.auditoria import Auditoria

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def listar_auditoria(
    skip: int = 0,
    limit: int = 100,
    id_caso: Optional[int] = None,
    id_usuario: Optional[int] = None,
    accion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Listar registros de auditoría con paginación y filtros opcionales.

    URL: GET /api/v1/auditoria?skip=0&limit=100&id_caso=1&id_usuario=2
    """
    query = db.query(Auditoria)

    if id_caso is not None:
        query = query.filter(Auditoria.id_caso == id_caso)

    if id_usuario is not None:
        query = query.filter(Auditoria.id_usuario == id_usuario)

    if accion:
        query = query.filter(Auditoria.accion.ilike(f"%{accion}%"))

    auditorias = query.order_by(Auditoria.timestamp.desc()).offset(skip).limit(limit).all()
    return auditorias


@router.get("/staff/{id_usuario}", status_code=status.HTTP_200_OK)
def listar_acciones_por_staff(
    id_usuario: int,
    skip: int = 0,
    limit: int = 100,
    id_caso: Optional[int] = None,
    accion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Consultar todas las acciones realizadas por un miembro específico del staff.

    URL: GET /api/v1/auditoria/staff/3?skip=0&limit=100
    """
    query = db.query(Auditoria).filter(Auditoria.id_usuario == id_usuario)

    if id_caso is not None:
        query = query.filter(Auditoria.id_caso == id_caso)

    if accion:
        query = query.filter(Auditoria.accion.ilike(f"%{accion}%"))

    acciones = query.order_by(Auditoria.timestamp.desc()).offset(skip).limit(limit).all()
    return acciones


@router.get("/{auditoria_id}", status_code=status.HTTP_200_OK)
def obtener_auditoria(
    auditoria_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un registro de auditoría por ID.

    URL: GET /api/v1/auditoria/5
    """
    auditoria = db.query(Auditoria).filter(Auditoria.id_auditoria == auditoria_id).first()

    if not auditoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro de auditoría con ID {auditoria_id} no encontrado"
        )

    return auditoria
