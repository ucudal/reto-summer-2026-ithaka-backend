from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.convocatoria import Convocatoria
from app.schemas.convocatoria import ConvocatoriaCreate, ConvocatoriaUpdate, ConvocatoriaResponse

router = APIRouter()


@router.get("/", response_model=List[ConvocatoriaResponse])
def listar_convocatorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Convocatoria).offset(skip).limit(limit).all()


@router.get("/{convocatoria_id}", response_model=ConvocatoriaResponse)
def obtener_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    convocatoria = (
        db.query(Convocatoria)
        .filter(Convocatoria.id_convocatoria == convocatoria_id)
        .first()
    )
    if not convocatoria:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return convocatoria


@router.post("/", response_model=ConvocatoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_convocatoria(convocatoria_data: ConvocatoriaCreate, db: Session = Depends(get_db)):
    nueva = Convocatoria(**convocatoria_data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{convocatoria_id}", response_model=ConvocatoriaResponse)
def actualizar_convocatoria(convocatoria_id: int, convocatoria_data: ConvocatoriaUpdate, db: Session = Depends(get_db)):
    convocatoria = (
        db.query(Convocatoria)
        .filter(Convocatoria.id_convocatoria == convocatoria_id)
        .first()
    )
    if not convocatoria:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")

    update_data = convocatoria_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(convocatoria, field, value)

    db.commit()
    db.refresh(convocatoria)
    return convocatoria


@router.delete("/{convocatoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    convocatoria = (
        db.query(Convocatoria)
        .filter(Convocatoria.id_convocatoria == convocatoria_id)
        .first()
    )
    if not convocatoria:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")

    db.delete(convocatoria)
    db.commit()
    return None
