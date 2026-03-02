"""Endpoints de auditoria (solo lectura).

Referencia de permisos: PERMISOS_POR_ROL.md.
- GET /auditoria: Admin y Coordinador.
- GET /auditoria/{id}: Admin y Coordinador.
- GET /auditoria/staff/{id_usuario}: Admin sin restriccion;
  Coordinador/Tutor solo su propio historial.

Contexto funcional:
- La auditoria registra cambios relevantes del sistema (crear/editar/eliminar).
- Este modulo solo expone consultas; no permite crear ni modificar auditorias.
- Se usa para trazabilidad operativa y revision de acciones del staff.

Origen de datos:
- Los registros se generan desde el servicio
  `app/services/auditoria_service.py`.
- En los endpoints de negocio se invocan principalmente:
  `registrar_auditoria_caso(...)` y `registrar_auditoria_general(...)`.
- Este endpoint solo consulta esos registros ya persistidos.
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
    """Lista todos los registros de auditoria.

    Permisos:
    - Admin y Coordinador: acceso completo.

    Nota:
    - El contenido listado fue creado por el service de auditoria
      durante operaciones de negocio en otros endpoints.
    """
    # Consulta simple de solo lectura, ordenada por ID ascendente
    # para reconstruir la secuencia historica de eventos.
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
    """Lista acciones de auditoria de un usuario del staff.

    Permisos:
    - Admin: puede consultar historial de cualquier usuario.
    - Coordinador y Tutor: solo su propio historial.
    """
    # 1) Regla de acceso condicional para historial personal.
    if current_user.rol.nombre_rol in ["Coordinador", "Tutor"]:
        if id_usuario != current_user.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes ver tu propio historial de acciones"
            )

    # 2) Query base por usuario.
    query = db.query(Auditoria).filter(Auditoria.id_usuario == id_usuario)

    # 3) Filtros opcionales.
    if id_caso is not None:
        query = query.filter(Auditoria.id_caso == id_caso)

    if accion:
        # Busqueda parcial, util para acciones como "nota_" o "caso_".
        query = query.filter(Auditoria.accion.ilike(f"%{accion}%"))

    # 4) Orden por eventos mas recientes + paginacion.
    acciones = query.order_by(Auditoria.timestamp.desc()).offset(skip).limit(limit).all()
    return acciones


@router.get("/{auditoria_id}", response_model=AuditoriaResponse, status_code=status.HTTP_200_OK)
def obtener_auditoria(
    auditoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    """Obtiene un registro de auditoria puntual por su ID.

    Permisos:
    - Admin y Coordinador: acceso completo.
    """
    # Consulta puntual por ID para inspeccionar un evento especifico.
    auditoria = db.query(Auditoria).filter(Auditoria.id_auditoria == auditoria_id).first()
    if not auditoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro de auditoría con ID {auditoria_id} no encontrado",
        )
    return auditoria
