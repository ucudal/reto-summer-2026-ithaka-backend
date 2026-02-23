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
from app.models.usuario import Usuario
from app.schemas.auditoria import AuditoriaResponse
from app.core.security import require_role

router = APIRouter()


@router.get("/", response_model=list[AuditoriaResponse], status_code=status.HTTP_200_OK)
def listar_auditoria(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    """
    Listar todos los registros de auditoría (Solo Admin y Coordinador)

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
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """
    Consultar todas las acciones realizadas por un miembro específico del staff.
    Coordinador y Tutor solo pueden ver sus propias acciones.

    URL: GET /api/v1/auditoria/staff/3?skip=0&limit=100
    """
    # Coordinador y Tutor solo pueden ver sus propias acciones
    if current_user.rol.nombre_rol in ["Coordinador", "Tutor"]:
        if id_usuario != current_user.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes ver tu propio historial de acciones"
            )
    
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
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    """
    Obtener un registro de auditoría por ID (Solo Admin y Coordinador)

    URL: GET /api/v1/auditoria/5
    """
    auditoria = db.query(Auditoria).filter(Auditoria.id_auditoria == auditoria_id).first()

    if not auditoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro de auditoría con ID {auditoria_id} no encontrado"
        )

    return auditoria
