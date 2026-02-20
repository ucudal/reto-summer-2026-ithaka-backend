from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.catalogo_estados import CatalogoEstados
from app.models.usuario import Usuario
from app.schemas.catalogo_estados import CatalogoEstadosCreate, CatalogoEstadosUpdate, CatalogoEstadosResponse
from app.core.security import require_role

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def listar_estados(
    skip: int = 0,
    limit: int = 100,
    tipo_caso: str = None,  # Filtrar por tipo: "Postulacion" o "Proyecto"
    db: Session = Depends(get_db)
):
    """Listar todos los estados"""
    query = db.query(CatalogoEstados)
    
    if tipo_caso:
        query = query.filter(CatalogoEstados.tipo_caso == tipo_caso)
    
    estados = query.offset(skip).limit(limit).all()
    return estados


@router.get("/{estado_id}", status_code=status.HTTP_200_OK, response_model=CatalogoEstadosResponse)
def obtener_estado(
    estado_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un estado por ID"""
    estado = db.query(CatalogoEstados).filter(
        CatalogoEstados.id_estado == estado_id
    ).first()
    
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estado con ID {estado_id} no encontrado"
        )
    
    return estado


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CatalogoEstadosResponse)
def crear_estado(
    estado_data: CatalogoEstadosCreate,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(require_role(["admin"]))  # TEMPORALMENTE DESACTIVADO - JWT
):
    nuevo_estado = CatalogoEstados(**estado_data.model_dump())
    db.add(nuevo_estado)
    db.commit()
    db.refresh(nuevo_estado)
    
    return nuevo_estado


@router.put("/{estado_id}", status_code=status.HTTP_200_OK, response_model=CatalogoEstadosResponse)
def actualizar_estado(
    estado_id: int,
    estado_data: CatalogoEstadosUpdate,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(require_role(["admin"]))  # TEMPORALMENTE DESACTIVADO - JWT
):
    estado = db.query(CatalogoEstados).filter(
        CatalogoEstados.id_estado == estado_id
    ).first()
    
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estado con ID {estado_id} no encontrado"
        )
    
    for campo, valor in estado_data.model_dump(exclude_unset=True).items():
        setattr(estado, campo, valor)
    
    db.commit()
    db.refresh(estado)
    
    return estado


@router.delete("/{estado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estado(
    estado_id: int,
    db: Session = Depends(get_db)
    # current_user: Usuario = Depends(require_role(["admin"]))  # TEMPORALMENTE DESACTIVADO - JWT
):
    estado = db.query(CatalogoEstados).filter(
        CatalogoEstados.id_estado == estado_id
    ).first()
    
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estado con ID {estado_id} no encontrado"
        )
    
    db.delete(estado)
    db.commit()
    
    return None
