from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db
from app.models import Caso, CatalogoEstados, Convocatoria, Apoyo, Programa
from app.models.usuario import Usuario
from app.models.asignacion import Asignacion
from app.models.emprendedor import Emprendedor
from app.schemas.caso import CasoCreate, CasoUpdate, CasoResponse
from app.core.security import require_role
from app.services.auditoria_service import registrar_auditoria_caso

router = APIRouter()


# ============================================================================
# LISTAR TODOS (GET /)
# ============================================================================
@router.get("/", response_model=List[CasoResponse])
def listar_casos(
    skip: int = 0,
    limit: int = 100,
    id_estado: int = None,
    tipo_caso: str = None,
    nombre_estado: str = None,
    id_emprendedor: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    query = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    )

    if current_user.rol.nombre_rol == "Tutor":
        query = query.join(Asignacion).filter(
            Asignacion.id_usuario == current_user.id_usuario
        )

    if id_estado:
        query = query.filter(Caso.id_estado == id_estado)
    if id_emprendedor:
        query = query.filter(Caso.id_emprendedor == id_emprendedor)
    if tipo_caso:
        query = query.join(Caso.estado).filter(CatalogoEstados.tipo_caso == tipo_caso)
    if nombre_estado:
        query = query.join(Caso.estado).filter(CatalogoEstados.nombre_estado == nombre_estado)

    casos = query.offset(skip).limit(limit).all()
    return casos


# ============================================================================
# OBTENER UNO (GET /{id})
# ============================================================================
@router.get("/{caso_id}", response_model=CasoResponse)
def obtener_caso(
    caso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    caso = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    ).filter(Caso.id_caso == caso_id).first()

    if not caso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caso no encontrado")

    if current_user.rol.nombre_rol == "Tutor":
        if not any(asig.id_usuario == current_user.id_usuario for asig in caso.asignaciones):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a este caso")

    return caso


# ============================================================================
# CREAR (POST /)
# ============================================================================
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CasoResponse)
def crear_caso(
    caso_data: CasoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    estado_postulado = db.query(CatalogoEstados).filter(
        func.lower(CatalogoEstados.nombre_estado) == "postulado",
        func.lower(CatalogoEstados.tipo_caso) == "postulacion"
    ).first()

    if not estado_postulado:
        estado_postulado = db.query(CatalogoEstados).filter(
            func.lower(CatalogoEstados.nombre_estado) == "postulado"
        ).first()

    if not estado_postulado:
        raise HTTPException(status_code=500, detail="No existe el estado por defecto 'Postulado'.")

    if caso_data.id_emprendedor:
        emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == caso_data.id_emprendedor).first()
        if not emprendedor:
            raise HTTPException(status_code=404, detail="Emprendedor no encontrado")

    nuevo_caso = Caso(**caso_data.model_dump(exclude={"id_estado"}), id_estado=estado_postulado.id_estado)
    db.add(nuevo_caso)
    db.flush()  # Obtener id antes del commit

    registrar_auditoria_caso(
        db=db,
        accion="Caso creado",
        id_usuario=current_user.id_usuario,
        id_caso=nuevo_caso.id_caso,
        valor_nuevo=f"Caso '{nuevo_caso.nombre_caso}' creado"
    )

    db.commit()
    db.refresh(nuevo_caso)
    return nuevo_caso


# ============================================================================
# ACTUALIZAR (PUT /{id})
# ============================================================================
@router.put("/{caso_id}", response_model=CasoResponse)
def actualizar_caso(
    caso_id: int,
    caso_data: CasoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    if current_user.rol.nombre_rol == "Tutor":
        if not any(asig.id_usuario == current_user.id_usuario for asig in caso.asignaciones):
            raise HTTPException(status_code=403, detail="No tienes acceso a este caso")

    valores_anteriores = {field: getattr(caso, field) for field in caso_data.model_dump(exclude_unset=True)}
    for field, value in caso_data.model_dump(exclude_unset=True).items():
        setattr(caso, field, value)

    if valores_anteriores:
        registrar_auditoria_caso(
            db=db,
            accion="Caso actualizado",
            id_usuario=current_user.id_usuario,
            id_caso=caso_id,
            valor_anterior=str(valores_anteriores),
            valor_nuevo=str(caso_data.model_dump(exclude_unset=True))
        )

    db.commit()
    db.refresh(caso)
    return caso


# ============================================================================
# CAMBIAR ESTADO (PUT /{id}/cambiar_estado)
# ============================================================================
@router.put("/{caso_id}/cambiar_estado", response_model=CasoResponse)
def cambiar_estado_caso(
    caso_id: int,
    nombre_estado: str,
    tipo_caso: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    estado_catalogo = db.query(CatalogoEstados).filter(
        CatalogoEstados.nombre_estado == nombre_estado,
        CatalogoEstados.tipo_caso == tipo_caso
    ).first()

    if not estado_catalogo:
        raise HTTPException(status_code=404, detail="Estado no existe para este tipo de caso")

    estado_anterior = caso.estado.nombre_estado if caso.estado else None
    caso.id_estado = estado_catalogo.id_estado

    registrar_auditoria_caso(
        db=db,
        accion="Cambio de estado",
        id_usuario=current_user.id_usuario,
        id_caso=caso_id,
        valor_anterior=f"{estado_anterior} ({caso.estado.tipo_caso})" if caso.estado else None,
        valor_nuevo=f"{nombre_estado} ({tipo_caso})"
    )

    db.commit()
    db.refresh(caso)
    return caso