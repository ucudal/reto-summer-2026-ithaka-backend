
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, ProgrammingError
from typing import List

from app.api.deps import get_db
from app.models.catalogo_apoyo import CatalogoApoyo
from app.schemas.catalogo_apoyos import CatalogoApoyosCreate, CatalogoApoyosUpdate, CatalogoApoyosResponse
from app.core.security import require_role

router = APIRouter()

# GET: Todos los roles
@router.get("/", response_model=List[CatalogoApoyosResponse], status_code=status.HTTP_200_OK)
def listar_catalogo_apoyos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    try:
        return db.query(CatalogoApoyo).offset(skip).limit(limit).all()
    except ProgrammingError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="La tabla catalogo_apoyo no existe en la base actual. Ejecuta el script de estructura de base de datos."
        )

# GET por ID
@router.get("/{apoyo_id}", response_model=CatalogoApoyosResponse, status_code=status.HTTP_200_OK)
def obtener_catalogo_apoyo(
    apoyo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    try:
        obj = db.query(CatalogoApoyo).filter(CatalogoApoyo.id_catalogo_apoyo == apoyo_id).first()
    except ProgrammingError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="La tabla catalogo_apoyo no existe en la base actual. Ejecuta el script de estructura de base de datos."
        )
    if not obj:
        raise HTTPException(status_code=404, detail="Catálogo de apoyo no encontrado")
    return obj

# POST: Solo admin
@router.post("/", response_model=CatalogoApoyosResponse, status_code=status.HTTP_201_CREATED)
def crear_catalogo_apoyo(
    catalogo_data: CatalogoApoyosCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin"]))
):
    nuevo = CatalogoApoyo(**catalogo_data.model_dump())
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "unique" in str(e.orig).lower():
            raise HTTPException(status_code=409, detail="Ya existe un catálogo de apoyo con ese nombre")
        raise HTTPException(status_code=400, detail=str(e.orig))
    except ProgrammingError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="La tabla catalogo_apoyo no existe en la base actual. Ejecuta el script de estructura de base de datos."
        )

    db.refresh(nuevo)
    return nuevo

# PUT: Solo admin
@router.put("/{apoyo_id}", response_model=CatalogoApoyosResponse, status_code=status.HTTP_200_OK)
def actualizar_catalogo_apoyo(
    apoyo_id: int,
    catalogo_data: CatalogoApoyosUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin"]))
):
    try:
        obj = db.query(CatalogoApoyo).filter(CatalogoApoyo.id_catalogo_apoyo == apoyo_id).first()
    except ProgrammingError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="La tabla catalogo_apoyo no existe en la base actual. Ejecuta el script de estructura de base de datos."
        )
    if not obj:
        raise HTTPException(status_code=404, detail="Catálogo de apoyo no encontrado")
    for campo, valor in catalogo_data.model_dump(exclude_unset=True).items():
        setattr(obj, campo, valor)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "unique" in str(e.orig).lower():
            raise HTTPException(status_code=409, detail="Ya existe un catálogo de apoyo con ese nombre")
        raise HTTPException(status_code=400, detail=str(e.orig))
    except ProgrammingError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="La tabla catalogo_apoyo no existe en la base actual. Ejecuta el script de estructura de base de datos."
        )

    db.refresh(obj)
    return obj

# DELETE: Solo admin
@router.delete("/{apoyo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_catalogo_apoyo(
    apoyo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin"]))
):
    try:
        obj = db.query(CatalogoApoyo).filter(CatalogoApoyo.id_catalogo_apoyo == apoyo_id).first()
    except ProgrammingError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="La tabla catalogo_apoyo no existe en la base actual. Ejecuta el script de estructura de base de datos."
        )
    if not obj:
        raise HTTPException(status_code=404, detail="Catálogo de apoyo no encontrado")
    db.delete(obj)
    db.commit()
    return None
