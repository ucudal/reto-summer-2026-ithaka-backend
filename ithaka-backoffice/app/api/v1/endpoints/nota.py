"""Endpoints de notas.

Referencia de permisos: PERMISOS_POR_ROL.md.
- GET listado/detalle: Tutor solo en casos asignados.
- POST: Admin, Coordinador y Tutor pueden crear.
- PUT/DELETE: Tutor solo sobre notas propias.
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
    return current_user.rol and current_user.rol.nombre_rol == _TUTOR_ROLE


def _obtener_nota_or_404(db: Session, nota_id: int) -> Nota:
    nota = db.query(Nota).filter(Nota.id_nota == nota_id).first()
    if nota is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada",
        )
    return nota


def _tutor_tiene_caso_asignado(db: Session, tutor_id: int, caso_id: int) -> bool:
    asignacion = db.query(Asignacion.id_asignacion).filter(
        Asignacion.id_caso == caso_id,
        Asignacion.id_usuario == tutor_id,
    ).first()
    return asignacion is not None


def _validar_tipo_nota(tipo_nota: Optional[str]) -> None:
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
    query = db.query(Nota)

    if _es_tutor(current_user):
        query = query.join(Asignacion, Nota.id_caso == Asignacion.id_caso).filter(
            Asignacion.id_usuario == current_user.id_usuario
        )

    if id_caso is not None:
        query = query.filter(Nota.id_caso == id_caso)

    if id_usuario is not None:
        query = query.filter(Nota.id_usuario == id_usuario)

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
    nota = _obtener_nota_or_404(db, nota_id)

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
    if _es_tutor(current_user) and nota_data.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes crear notas con tu propio usuario",
        )

    _validar_tipo_nota(nota_data.tipo_nota)

    nueva_nota = Nota(**nota_data.model_dump())
    db.add(nueva_nota)

    try:
        db.flush()
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
    nota = _obtener_nota_or_404(db, nota_id)

    if _es_tutor(current_user) and nota.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes actualizar tus propias notas",
        )

    update_data = nota_data.model_dump(exclude_unset=True)
    if not update_data:
        return nota

    _validar_tipo_nota(update_data.get("tipo_nota"))

    if _es_tutor(current_user):
        if "id_usuario" in update_data and update_data["id_usuario"] != current_user.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes reasignar el autor de la nota",
            )

        if "id_caso" in update_data and not _tutor_tiene_caso_asignado(
            db, current_user.id_usuario, update_data["id_caso"]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso al caso indicado",
            )

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
    nota = _obtener_nota_or_404(db, nota_id)

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

    db.delete(nota)
    registrar_auditoria_caso(
        db=db,
        accion="nota_eliminada",
        id_usuario=id_usuario,
        id_caso=id_caso,
        valor_anterior=valor_anterior,
    )

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible eliminar la nota.",
        )

    return None
