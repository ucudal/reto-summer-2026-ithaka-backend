from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Caso
from app.models import CatalogoEstados
from app.models.usuario import Usuario
from app.schemas.caso import CasoCreate, CasoUpdate, CasoResponse
from app.core.security import get_current_user, require_role

router = APIRouter()


# ============================================================================
# LISTAR TODOS (GET /)
# ============================================================================
@router.get("/")
def listar_casos(
    skip: int = 0,
    limit: int = 100,
    id_estado: int = None,
    tipo_caso: str = None,
    nombre_estado: str = None,
    id_emprendedor: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar todos los casos
    
    URL: GET /api/v1/caso?skip=0&limit=100
    """
    query = db.query(Caso)
    if tipo_caso:
        query = query.join(CatalogoEstados).filter(CatalogoEstados.tipo_caso == tipo_caso)
    if nombre_estado:
        query = query.join(CatalogoEstados).filter(CatalogoEstados.nombre_estado == nombre_estado)
    if id_emprendedor:
        query = query.filter(Caso.id_emprendedor == id_emprendedor)
    if id_estado:
        query = query.filter(Caso.id_estado == id_estado)
    casos = query.offset(skip).limit(limit).all()
    return {"casos": casos}


# ============================================================================
# OBTENER UNO (GET /{id})
# ============================================================================
@router.get("/{caso_id}")
def obtener_caso(
    caso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener un caso específico por ID
    
    URL: GET /api/v1/casos/5
    """
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso {caso_id} no encontrado"
        )
    
    return caso


# ============================================================================
# CREAR (POST /)
# ============================================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_caso(
    caso_data: CasoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crear un nuevo caso
    
    URL: POST /api/v1/casos
    
    Body ejemplo:
    {
        "campo1": "valor1",
        "campo2": "valor2"
    }
    """
    nuevo_caso = Caso(**caso_data.model_dump())
    db.add(nuevo_caso)
    db.commit()
    db.refresh(nuevo_caso)
    return nuevo_caso


# ============================================================================
# ACTUALIZAR (PUT /{id})
# ============================================================================
@router.put("/{caso_id}")
def actualizar_caso(
    caso_id: int,
    caso_data: CasoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualizar un recurso existente
    
    URL: PUT /api/v1/casos/5
    """
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    update_data = caso_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(caso, field, value)
    
    db.commit()
    db.refresh(caso)
    return caso


# ============================================================================
# ELIMINAR (DELETE /{id})
# ============================================================================
@router.delete("/{caso_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_caso(
    caso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["admin"]))
):
    """
    Eliminar un caso
    
    URL: DELETE /api/v1/casos/5
    """
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    db.delete(caso)
    db.commit()
    return None



# ============================================================================
# ENDPOINTS PERSONALIZADOS (OPCIONALES)
# ============================================================================

@router.put("/{caso_id}/cambiar_estado")
def cambiar_estado_caso(
    caso_id: int,
    nombre_estado: str,  # "En Revisión", "Aprobado", etc
    tipo_caso: str,      # "Postulacion" o "Proyecto"
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cambiar el estado de un caso
    
    URL: PUT /api/v1/casos/5/cambiar_estado?nombre_estado=Aprobado&tipo_caso=Proyecto
    """
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    estado_catalogo = db.query(CatalogoEstados).filter(
        CatalogoEstados.nombre_estado == nombre_estado,
        CatalogoEstados.tipo_caso == tipo_caso
    ).first()
    
    if not estado_catalogo:
        raise HTTPException(
            status_code=404, 
            detail=f"Estado '{nombre_estado}' no existe para tipo '{tipo_caso}'"
        )
    
    caso.id_estado = estado_catalogo.id_estado
    db.commit()
    db.refresh(caso)
    
    return caso



