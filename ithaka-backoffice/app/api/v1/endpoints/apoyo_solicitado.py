"""
ENDPOINTS APOYO_SOLICITADO
===========================
Gestión de categorías de apoyo solicitadas por casos de emprendimiento.

Un caso puede solicitar múltiples categorías de apoyo.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.apoyo_solicitado import ApoyoSolicitado
from app.models.caso import Caso
from app.schemas.apoyo_solicitado import (
    ApoyoSolicitadoCreate,
    ApoyoSolicitadoUpdate,
    ApoyoSolicitadoResponse
)

router = APIRouter()


# ============================================================================
# LISTAR TODOS (GET /)
# ============================================================================
@router.get("/", response_model=List[ApoyoSolicitadoResponse])
def listar_apoyos_solicitados(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar todos los apoyos solicitados con paginación
    
    **Parámetros:**
    - skip: Cantidad de registros a saltar (paginación)
    - limit: Cantidad máxima de registros a retornar
    """
    apoyos = db.query(ApoyoSolicitado).offset(skip).limit(limit).all()
    return apoyos


# ============================================================================
# OBTENER POR CASO (GET /caso/{id_caso})
# ============================================================================
@router.get("/caso/{id_caso}", response_model=List[ApoyoSolicitadoResponse])
def listar_apoyos_por_caso(
    id_caso: int,
    db: Session = Depends(get_db)
):
    """
    Listar todos los apoyos solicitados para un caso específico
    
    **Parámetros:**
    - id_caso: ID del caso
    
    **Retorna:**
    - Lista de apoyos solicitados para ese caso
    """
    # Verificar que el caso existe
    caso = db.query(Caso).filter(Caso.id_caso == id_caso).first()
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso {id_caso} no encontrado"
        )
    
    apoyos = db.query(ApoyoSolicitado).filter(
        ApoyoSolicitado.id_caso == id_caso
    ).all()
    
    return apoyos


# ============================================================================
# OBTENER UNO (GET /{id})
# ============================================================================
@router.get("/{apoyo_solicitado_id}", response_model=ApoyoSolicitadoResponse)
def obtener_apoyo_solicitado(
    apoyo_solicitado_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un apoyo solicitado específico por ID
    
    **Parámetros:**
    - apoyo_solicitado_id: ID del apoyo solicitado
    """
    apoyo = db.query(ApoyoSolicitado).filter(
        ApoyoSolicitado.id_apoyo_solicitado == apoyo_solicitado_id
    ).first()
    
    if not apoyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apoyo solicitado {apoyo_solicitado_id} no encontrado"
        )
    
    return apoyo


# ============================================================================
# CREAR (POST /)
# ============================================================================
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApoyoSolicitadoResponse)
def crear_apoyo_solicitado(
    apoyo_data: ApoyoSolicitadoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo apoyo solicitado
    
    **Body ejemplo:**
    ```json
    {
        "categoria_apoyo": "Mentoría técnica",
        "id_caso": 1
    }
    ```
    
    **Validaciones:**
    - El caso debe existir
    - categoria_apoyo es obligatorio (1-150 caracteres)
    """
    # Verificar que el caso existe
    caso = db.query(Caso).filter(Caso.id_caso == apoyo_data.id_caso).first()
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso {apoyo_data.id_caso} no encontrado"
        )
    
    # Crear el apoyo solicitado
    nuevo_apoyo = ApoyoSolicitado(**apoyo_data.model_dump())
    db.add(nuevo_apoyo)
    db.commit()
    db.refresh(nuevo_apoyo)
    
    return nuevo_apoyo


# ============================================================================
# ACTUALIZAR (PUT /{id})
# ============================================================================
@router.put("/{apoyo_solicitado_id}", response_model=ApoyoSolicitadoResponse)
def actualizar_apoyo_solicitado(
    apoyo_solicitado_id: int,
    apoyo_data: ApoyoSolicitadoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un apoyo solicitado existente
    
    **Body ejemplo:**
    ```json
    {
        "categoria_apoyo": "Mentoría técnica avanzada"
    }
    ```
    
    **Notas:**
    - Solo se puede actualizar la categoría de apoyo
    - No se puede cambiar el caso asociado
    """
    # Buscar el apoyo solicitado
    apoyo = db.query(ApoyoSolicitado).filter(
        ApoyoSolicitado.id_apoyo_solicitado == apoyo_solicitado_id
    ).first()
    
    if not apoyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apoyo solicitado {apoyo_solicitado_id} no encontrado"
        )
    
    # Actualizar solo los campos enviados
    update_data = apoyo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(apoyo, field, value)
    
    db.commit()
    db.refresh(apoyo)
    
    return apoyo


# ============================================================================
# ELIMINAR (DELETE /{id})
# ============================================================================
@router.delete("/{apoyo_solicitado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_apoyo_solicitado(
    apoyo_solicitado_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un apoyo solicitado
    
    **Parámetros:**
    - apoyo_solicitado_id: ID del apoyo solicitado a eliminar
    
    **Retorna:**
    - 204 No Content si se eliminó exitosamente
    - 404 Not Found si no existe
    """
    apoyo = db.query(ApoyoSolicitado).filter(
        ApoyoSolicitado.id_apoyo_solicitado == apoyo_solicitado_id
    ).first()
    
    if not apoyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apoyo solicitado {apoyo_solicitado_id} no encontrado"
        )
    
    db.delete(apoyo)
    db.commit()
    
    return None
