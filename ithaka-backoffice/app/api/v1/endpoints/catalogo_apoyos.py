
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
    return db.query(CatalogoApoyo).offset(skip).limit(limit).all()

# GET por ID
@router.get("/{apoyo_id}", response_model=CatalogoApoyosResponse, status_code=status.HTTP_200_OK)
def obtener_catalogo_apoyo(
    apoyo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    obj = db.query(CatalogoApoyo).filter(CatalogoApoyo.id_catalogo_apoyo == apoyo_id).first()
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
    db.commit()
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
    obj = db.query(CatalogoApoyo).filter(CatalogoApoyo.id_catalogo_apoyo == apoyo_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Catálogo de apoyo no encontrado")
    for campo, valor in catalogo_data.model_dump(exclude_unset=True).items():
        setattr(obj, campo, valor)
    db.commit()
    db.refresh(obj)
    return obj

# DELETE: Solo admin
@router.delete("/{apoyo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_catalogo_apoyo(
    apoyo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Admin"]))
):
    obj = db.query(CatalogoApoyo).filter(CatalogoApoyo.id_catalogo_apoyo == apoyo_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Catálogo de apoyo no encontrado")
    db.delete(obj)
    db.commit()
    return None
