"""
TEMPLATE PARA CREAR NUEVOS ENDPOINTS
=====================================

Este es un template que pueden copiar para crear nuevos archivos de endpoints.

PASOS PARA USAR ESTE TEMPLATE:
1. Copiar este archivo
2. Renombrarlo (ej: casos.py, usuarios.py, convocatorias.py)
3. Buscar y reemplazar "RECURSO" por tu recurso (ej: "Caso", "Usuario")
4. Buscar y reemplazar "recurso" por tu recurso en minúscula
5. Importar el router en app/api/v1/api.py
6. Crear los schemas correspondientes en app/schemas/

EJEMPLO:
    Si vas a crear endpoints para "Caso":
    - RECURSO → Caso
    - recurso → caso
    - recursos → casos
"""

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
@router.get("/", status_code=status.HTTP_200_OK)
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
@router.get("/{recurso_id}", status_code=status.HTTP_200_OK)
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
@router.put("/{recurso_id}", status_code=status.HTTP_200_OK)
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


# ============================================================================
# TIPS IMPORTANTES
# ============================================================================
#
# 1. STATUS CODES comunes:
#    - 200 OK: Operación exitosa
#    - 201 Created: Recurso creado
#    - 204 No Content: Eliminación exitosa (sin body)
#    - 400 Bad Request: Datos inválidos
#    - 401 Unauthorized: No autenticado
#    - 403 Forbidden: No autorizado (sin permisos)
#    - 404 Not Found: Recurso no existe
#    - 500 Internal Server Error: Error del servidor
#
# 2. PARÁMETROS:
#    - Path params: /{recurso_id} → def func(recurso_id: int)
#    - Query params: ?skip=0&limit=10 → def func(skip: int = 0, limit: int = 10)
#    - Body: JSON en el request → def func(data: Schema)
#
# 3. DEPENDENCIES:
#    - db: Session = Depends(get_db) → Siempre para acceder a la DB
#    - current_user = Depends(get_current_user) → Para autenticación
#    - admin = Depends(require_admin) → Para autorización
#
# 4. BÚSQUEDAS CON FILTROS:
#    db.query(Model).filter(
#        Model.campo1 == valor1,
#        Model.campo2.like(f"%{busqueda}%")
#    ).all()
#
# 5. JOINS:
#    db.query(Caso).join(Emprendedor).filter(
#        Emprendedor.email == "test@example.com"
#    ).all()
