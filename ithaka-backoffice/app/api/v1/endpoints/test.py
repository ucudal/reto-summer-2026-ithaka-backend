from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
# from app.models import RECURSO
# from app.schemas.recurso import RECURSOCreate, RECURSOUpdate, RECURSOResponse

router = APIRouter()


# ============================================================================
# LISTAR TODOS (GET /)
# ============================================================================
@router.get("/")
def listar_recursos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar todos los recursos con paginación
    
    URL: GET /api/v1/recursos?skip=0&limit=100
    """
    # recursos = db.query(RECURSO).offset(skip).limit(limit).all()
    # return recursos
    return {"mensaje": "Implementar query"}


# ============================================================================
# OBTENER UNO (GET /{id})
# ============================================================================
@router.get("/{recurso_id}")
def obtener_recurso(
    recurso_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un recurso específico por ID
    
    URL: GET /api/v1/recursos/5
    """
    # recurso = db.query(RECURSO).filter(RECURSO.id_recurso == recurso_id).first()
    # 
    # if not recurso:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Recurso {recurso_id} no encontrado"
    #     )
    # 
    # return recurso
    return {"mensaje": "Implementar búsqueda"}


# ============================================================================
# CREAR (POST /)
# ============================================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_recurso(
    # recurso_data: RECURSOCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo recurso
    
    URL: POST /api/v1/recursos
    
    Body ejemplo:
    {
        "campo1": "valor1",
        "campo2": "valor2"
    }
    """
    # nuevo_recurso = RECURSO(**recurso_data.dict())
    # db.add(nuevo_recurso)
    # db.commit()
    # db.refresh(nuevo_recurso)
    # return nuevo_recurso
    return {"mensaje": "Implementar creación"}


# ============================================================================
# ACTUALIZAR (PUT /{id})
# ============================================================================
@router.put("/{recurso_id}")
def actualizar_recurso(
    recurso_id: int,
    # recurso_data: RECURSOUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un recurso existente
    
    URL: PUT /api/v1/recursos/5
    """
    # recurso = db.query(RECURSO).filter(RECURSO.id_recurso == recurso_id).first()
    # 
    # if not recurso:
    #     raise HTTPException(status_code=404, detail="Recurso no encontrado")
    # 
    # update_data = recurso_data.dict(exclude_unset=True)
    # for field, value in update_data.items():
    #     setattr(recurso, field, value)
    # 
    # db.commit()
    # db.refresh(recurso)
    # return recurso
    return {"mensaje": "Implementar actualización"}


# ============================================================================
# ELIMINAR (DELETE /{id})
# ============================================================================
@router.delete("/{recurso_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_recurso(
    recurso_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un recurso
    
    URL: DELETE /api/v1/recursos/5
    """
    # recurso = db.query(RECURSO).filter(RECURSO.id_recurso == recurso_id).first()
    # 
    # if not recurso:
    #     raise HTTPException(status_code=404, detail="Recurso no encontrado")
    # 
    # db.delete(recurso)
    # db.commit()
    # return None
    return {"mensaje": "Implementar eliminación"}


# ============================================================================
# ENDPOINTS PERSONALIZADOS (OPCIONALES)
# ============================================================================

@router.get("/{recurso_id}/relacionados")
def obtener_relacionados(
    recurso_id: int,
    db: Session = Depends(get_db)
):
    """
    Ejemplo de endpoint personalizado
    
    URL: GET /api/v1/recursos/5/relacionados
    """
    return {"mensaje": "Implementar lógica personalizada"}

