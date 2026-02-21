"""
Endpoints NOTA
--------------
TODO: Implementar usando TEMPLATE.py como guia

Endpoints a crear:
- GET /api/v1/notas - Listar todas
- GET /api/v1/notas/{id} - Obtener una
- POST /api/v1/notas - Crear
- PUT /api/v1/notas/{id} - Actualizar
- DELETE /api/v1/notas/{id} - Eliminar
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.nota import Nota
from app.schemas.nota import NotaCreate, NotaUpdate
from app.services.auditoria_service import registrar_auditoria_caso

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def listar_notas(
    skip: int = 0,
    limit: int = 100,
    id_caso: Optional[int] = None,
    id_usuario: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Listar notas con paginacion y filtros opcionales.

    URL: GET /api/v1/notas?skip=0&limit=100&id_caso=1&id_usuario=2
    """
    query = db.query(Nota)

    if id_caso is not None:
        query = query.filter(Nota.id_caso == id_caso)

    if id_usuario is not None:
        query = query.filter(Nota.id_usuario == id_usuario)

    notas = query.order_by(Nota.fecha.desc()).offset(skip).limit(limit).all()
    return notas


@router.get("/{nota_id}", status_code=status.HTTP_200_OK)
def obtener_nota(
    nota_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una nota por ID.

    URL: GET /api/v1/notas/5
    """
    nota = db.query(Nota).filter(Nota.id_nota == nota_id).first()

    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada"
        )

    return nota


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_nota(
    nota_data: NotaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva nota.

    URL: POST /api/v1/notas
    """
    nueva_nota = Nota(**nota_data.model_dump())
    db.add(nueva_nota)
    db.flush()

    registrar_auditoria_caso(
        db=db,
        accion="nota_creada",
        id_usuario=nueva_nota.id_usuario,
        id_caso=nueva_nota.id_caso,
        valor_nuevo={
            "id_nota": nueva_nota.id_nota,
            "contenido": nueva_nota.contenido,
            "id_usuario": nueva_nota.id_usuario,
            "id_caso": nueva_nota.id_caso,
        },
    )

    db.commit()
    db.refresh(nueva_nota)

    return nueva_nota


@router.put("/{nota_id}", status_code=status.HTTP_200_OK)
def actualizar_nota(
    nota_id: int,
    nota_data: NotaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una nota existente.

    URL: PUT /api/v1/notas/5
    """
    nota = db.query(Nota).filter(Nota.id_nota == nota_id).first()

    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada"
        )

    update_data = nota_data.model_dump(exclude_unset=True)
    if not update_data:
        return nota

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

    db.commit()
    db.refresh(nota)

    return nota


@router.delete("/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_nota(
    nota_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una nota.

    URL: DELETE /api/v1/notas/5
    """
    nota = db.query(Nota).filter(Nota.id_nota == nota_id).first()

    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada"
        )

    valor_anterior = {
        "id_nota": nota.id_nota,
        "contenido": nota.contenido,
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

    db.commit()

    return None
