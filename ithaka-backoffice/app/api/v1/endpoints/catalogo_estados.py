from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models.catalogo_estados import CatalogoEstados
from app.models.usuario import Usuario
from app.schemas.catalogo_estados import CatalogoEstadosCreate, CatalogoEstadosUpdate, CatalogoEstadosResponse
from app.core.security import require_role

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CatalogoEstadosResponse])
def listar_estados(
    skip: int = 0,
    limit: int = 100,
    tipo_caso: str = None,  # Filtrar por tipo: "postulacion" o "proyecto"
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """Listar todos los estados (todos los roles) y devolver campos en minúscula"""
    query = db.query(CatalogoEstados)
    
    if tipo_caso:
        query = query.filter(func.lower(CatalogoEstados.tipo_caso) == tipo_caso.lower())
    
    estados = query.offset(skip).limit(limit).all()

    # Normalizar salida: asegurarse que nombre_estado y tipo_caso estén en minúscula
    estados_normalizados = []
    for e in estados:
        estados_normalizados.append({
            "id_estado": e.id_estado,
            "nombre_estado": e.nombre_estado.lower() if isinstance(e.nombre_estado, str) else e.nombre_estado,
            "tipo_caso": e.tipo_caso.lower() if isinstance(e.tipo_caso, str) else e.tipo_caso
        })

    return estados_normalizados


@router.get("/{estado_id}", status_code=status.HTTP_200_OK, response_model=CatalogoEstadosResponse)
def obtener_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """Obtener un estado por ID (todos los roles) y devolver campos en minúscula"""
    estado = db.query(CatalogoEstados).filter(
        CatalogoEstados.id_estado == estado_id
    ).first()
    
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estado con ID {estado_id} no encontrado"
        )
    
    estado_normalizado = {
        "id_estado": estado.id_estado,
        "nombre_estado": estado.nombre_estado.lower() if isinstance(estado.nombre_estado, str) else estado.nombre_estado,
        "tipo_caso": estado.tipo_caso.lower() if isinstance(estado.tipo_caso, str) else estado.tipo_caso
    }

    return estado_normalizado


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CatalogoEstadosResponse)
def crear_estado(
    estado_data: CatalogoEstadosCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """Crear estado (Solo Admin)"""
    nuevo_estado = CatalogoEstados(**estado_data.model_dump())
    db.add(nuevo_estado)
    db.commit()
    db.refresh(nuevo_estado)
    
    return nuevo_estado


@router.put("/{estado_id}", status_code=status.HTTP_200_OK, response_model=CatalogoEstadosResponse)
def actualizar_estado(
    estado_id: int,
    estado_data: CatalogoEstadosUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """Actualizar estado (Solo Admin)"""
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
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """Eliminar estado (Solo Admin)"""
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