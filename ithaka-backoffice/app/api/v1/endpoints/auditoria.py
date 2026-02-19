"""
Endpoints AUDITORIA
-------------------
Registro de eventos para trazabilidad del sistema.

Endpoints expuestos:
- GET /api/v1/auditoria - Listar todos los registros
- GET /api/v1/auditoria/{id} - Obtener un registro
- GET /api/v1/auditoria/staff/{id_usuario} - Acciones de un miembro del staff

NOTA: Los registros de auditoría son de solo lectura en API pública.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.auditoria import Auditoria
from app.schemas.auditoria import AuditoriaResponse

router = APIRouter()


@router.get("/", response_model=list[AuditoriaResponse], status_code=status.HTTP_200_OK)
def listar_auditoria(
    db: Session = Depends(get_db)
):
    """
    Listar todos los registros de auditoría.

    URL: GET /api/v1/auditoria
    """
    auditorias = db.query(Auditoria).order_by(Auditoria.id_auditoria.asc()).all()
    return auditorias


@router.get("/staff/{id_usuario}", response_model=list[AuditoriaResponse], status_code=status.HTTP_200_OK)
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


@router.get("/{auditoria_id}", response_model=AuditoriaResponse, status_code=status.HTTP_200_OK)
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
