"""Endpoints de notas.

Referencia de permisos: PERMISOS_POR_ROL.md.
- GET listado/detalle: Tutor solo en casos asignados.
- POST: Admin, Coordinador y Tutor pueden crear.
- PUT/DELETE: Tutor solo sobre notas propias.

Contexto funcional:
- Una "nota" es un registro de seguimiento asociado a un caso.
- Se usa para dejar observaciones de avance, bloqueos o acciones realizadas.
- Cada cambio relevante se registra en auditoria para trazabilidad.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import require_role
from app.models.asignacion import Asignacion
from app.models.nota import Nota
from app.models.usuario import Usuario
from app.schemas.nota import NotaCreate, NotaResponse, NotaUpdate
from app.services.auditoria_service import registrar_auditoria_caso

router = APIRouter()

_TUTOR_ROLE = "Tutor"
_ALLOWED_ROLES = ["Admin", "Coordinador", "Tutor"]


def _es_tutor(current_user: Usuario) -> bool:
    """Determina si el usuario autenticado tiene rol Tutor."""
    return current_user.rol and current_user.rol.nombre_rol == _TUTOR_ROLE


def _obtener_nota_or_404(db: Session, nota_id: int) -> Nota:
    """Obtiene una nota por id o responde 404 si no existe."""
    nota = db.query(Nota).filter(Nota.id_nota == nota_id).first()
    if nota is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada",
        )
    return nota


def _tutor_tiene_caso_asignado(db: Session, tutor_id: int, caso_id: int) -> bool:
    """Verifica si el Tutor esta asignado al caso indicado."""
    asignacion = db.query(Asignacion.id_asignacion).filter(
        Asignacion.id_caso == caso_id,
        Asignacion.id_usuario == tutor_id,
    ).first()
    return asignacion is not None


def _validar_tipo_nota(tipo_nota: Optional[str]) -> None:
    """Valida que tipo_nota tenga contenido util (no vacio)."""
    if tipo_nota is not None and not tipo_nota.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo 'tipo_nota' es obligatorio.",
        )


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[NotaResponse])
def listar_notas(
    skip: int = 0,
    limit: int = 100,
    id_caso: Optional[int] = None,
    id_usuario: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(_ALLOWED_ROLES)),
):
    """Lista notas con filtros opcionales y paginacion.

    Permisos:
    - Admin y Coordinador: acceso completo.
    - Tutor: solo notas de casos asignados.
    """
    # 1) Se arma la consulta base.
    query = db.query(Nota)

    # 2) Si es Tutor, se restringe a sus casos asignados.
    if _es_tutor(current_user):
        query = query.join(Asignacion, Nota.id_caso == Asignacion.id_caso).filter(
            Asignacion.id_usuario == current_user.id_usuario
        )

    # 3) Se aplican filtros opcionales enviados por query params.
    if id_caso is not None:
        query = query.filter(Nota.id_caso == id_caso)

    if id_usuario is not None:
        query = query.filter(Nota.id_usuario == id_usuario)

    # Orden cronológico descendente + paginación.
    return query.order_by(Nota.fecha.desc()).offset(skip).limit(limit).all()


@router.get("/{nota_id}", status_code=status.HTTP_200_OK, response_model=NotaResponse)
def obtener_nota(
    nota_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(_ALLOWED_ROLES)),
):
    """Obtiene una nota por ID.

    Permisos:
    - Admin y Coordinador: acceso completo.
    - Tutor: solo si el caso de la nota esta asignado.
    """
    # 1) Busca la nota o corta con 404.
    nota = _obtener_nota_or_404(db, nota_id)

    # 2) Control adicional para Tutor sobre el caso asociado.
    if _es_tutor(current_user) and not _tutor_tiene_caso_asignado(
        db, current_user.id_usuario, nota.id_caso
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta nota",
        )

    return nota


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NotaResponse)
def crear_nota(
    nota_data: NotaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(_ALLOWED_ROLES)),
):
    """Crea una nota.

    Permisos:
    - Admin, Coordinador y Tutor pueden crear.
    - Si es Tutor, `id_usuario` debe coincidir con el usuario autenticado.
    - No se exige asignacion previa del caso para crear.
    """
    # 1) Regla de seguridad: Tutor no puede crear notas en nombre de otro usuario.
    if _es_tutor(current_user) and nota_data.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes crear notas con tu propio usuario",
        )

    # 2) Validacion de dominio.
    _validar_tipo_nota(nota_data.tipo_nota)

    # 3) Alta de la entidad en la sesion SQLAlchemy.
    nueva_nota = Nota(**nota_data.model_dump())
    db.add(nueva_nota)

    try:
        # Flush para obtener id_nota antes de auditar.
        db.flush()
        # La auditoría queda en la misma transacción.
        registrar_auditoria_caso(
            db=db,
            accion="nota_creada",
            id_usuario=nueva_nota.id_usuario,
            id_caso=nueva_nota.id_caso,
            valor_nuevo={
                "id_nota": nueva_nota.id_nota,
                "contenido": nueva_nota.contenido,
                "tipo_nota": nueva_nota.tipo_nota,
                "id_usuario": nueva_nota.id_usuario,
                "id_caso": nueva_nota.id_caso,
            },
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuario o caso invalido.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible crear la nota.",
        )

    db.refresh(nueva_nota)
    return nueva_nota


@router.put("/{nota_id}", status_code=status.HTTP_200_OK, response_model=NotaResponse)
def actualizar_nota(
    nota_id: int,
    nota_data: NotaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(_ALLOWED_ROLES)),
):
    """Actualiza una nota existente.

    Permisos:
    - Admin y Coordinador: acceso completo.
    - Tutor: solo notas propias.
    """
    # 1) Busca la nota objetivo.
    nota = _obtener_nota_or_404(db, nota_id)

    # 2) Regla de seguridad para Tutor.
    if _es_tutor(current_user) and nota.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes actualizar tus propias notas",
        )

    # 3) Update parcial: solo campos enviados en el body.
    update_data = nota_data.model_dump(exclude_unset=True)
    if not update_data:
        return nota

    _validar_tipo_nota(update_data.get("tipo_nota"))

    if _es_tutor(current_user):
        # Tutor no puede reasignar la autoría a otro usuario.
        if "id_usuario" in update_data and update_data["id_usuario"] != current_user.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes reasignar el autor de la nota",
            )

        # Si cambia de caso, el nuevo caso debe estar asignado al Tutor.
        if "id_caso" in update_data and not _tutor_tiene_caso_asignado(
            db, current_user.id_usuario, update_data["id_caso"]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso al caso indicado",
            )

    # 4) Antes/despues para auditoria de cambios.
    valor_anterior = {field: getattr(nota, field) for field in update_data.keys()}

    for field, value in update_data.items():
        setattr(nota, field, value)

    valor_nuevo = {field: getattr(nota, field) for field in update_data.keys()}

    registrar_auditoria_caso(
        db=db,
        accion="nota_actualizada",
        id_usuario=nota.id_usuario,
        id_caso=nota.id_caso,
        valor_anterior=valor_anterior,
        valor_nuevo=valor_nuevo,
    )

    try:
        db.commit()
        db.refresh(nota)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuario o caso invalido.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible actualizar la nota.",
        )

    return nota


@router.delete("/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_nota(
    nota_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(_ALLOWED_ROLES)),
):
    """Elimina una nota.

    Permisos:
    - Admin y Coordinador: acceso completo.
    - Tutor: solo notas propias.
    """
    # 1) Busca la nota a eliminar.
    nota = _obtener_nota_or_404(db, nota_id)

    # 2) Regla de seguridad para Tutor.
    if _es_tutor(current_user) and nota.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes eliminar tus propias notas",
        )

    valor_anterior = {
        "id_nota": nota.id_nota,
        "contenido": nota.contenido,
        "tipo_nota": nota.tipo_nota,
        "id_usuario": nota.id_usuario,
        "id_caso": nota.id_caso,
    }

    id_usuario = nota.id_usuario
    id_caso = nota.id_caso

    # 3) Elimina y registra auditoria en una misma transaccion.
    db.delete(nota)
    registrar_auditoria_caso(
        db=db,
        accion="nota_eliminada",
        id_usuario=id_usuario,
        id_caso=id_caso,
        valor_anterior=valor_anterior,
    )

    try:
        # 4) Confirmar eliminacion + auditoria.
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible eliminar la nota.",
        )

    return None
