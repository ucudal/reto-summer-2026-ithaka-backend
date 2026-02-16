"""
ENDPOINTS: EMPRENDEDORES
========================
Este archivo maneja todas las operaciones CRUD de emprendedores.

CRUD = Create, Read, Update, Delete
- Create → POST   /emprendedores
- Read   → GET    /emprendedores  (lista)
          GET    /emprendedores/{id}  (uno específico)
- Update → PUT    /emprendedores/{id}
- Delete → DELETE /emprendedores/{id}
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Imports de tu aplicación
from app.api.deps import get_db
from app.models import Emprendedor
from app.schemas.emprendedor import EmprendedorCreate, EmprendedorUpdate, EmprendedorResponse

# ============================================================================
# CREAR EL ROUTER
# ============================================================================
# Este router se incluirá en api.py con el prefijo "/emprendedores"
router = APIRouter()


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/", status_code=status.HTTP_200_OK)
def listar_emprendedores(
    skip: int = 0,              # Parámetro de query: ?skip=0
    limit: int = 100,           # Parámetro de query: ?limit=100
    db: Session = Depends(get_db)  # Dependency: obtiene la sesión de DB
):
    """
    Listar todos los emprendedores con paginación
    
    URL final: GET /api/v1/emprendedores?skip=0&limit=100
    
    Parámetros:
    - skip: Cuántos registros saltear (para paginación)
    - limit: Máximo de registros a devolver
    - db: Sesión de base de datos (se inyecta automáticamente)
    
    Returns:
    - Lista de emprendedores
    
    Ejemplo de uso desde el frontend:
        fetch('/api/v1/emprendedores?skip=0&limit=10')
    """
    # Query a la base de datos
    emprendedores = db.query(Emprendedor).offset(skip).limit(limit).all()
    
    return emprendedores
    
    # NOTA: Cuando crees los schemas, usa esto en su lugar:
    # return [EmprendedorResponse.from_orm(e) for e in emprendedores]


@router.get("/{emprendedor_id}", status_code=status.HTTP_200_OK)
def obtener_emprendedor(
    emprendedor_id: int,  # Parámetro de ruta: /emprendedores/5
    db: Session = Depends(get_db)
):
    """
    Obtener un emprendedor específico por ID
    
    URL final: GET /api/v1/emprendedores/5
    
    Parámetros:
    - emprendedor_id: ID del emprendedor a buscar
    - db: Sesión de base de datos
    
    Returns:
    - Emprendedor encontrado
    - Error 404 si no existe
    """
    # Buscar el emprendedor
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == emprendedor_id
    ).first()
    
    # Si no existe, devolver error 404
    if not emprendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emprendedor con ID {emprendedor_id} no encontrado"
        )
    
    return emprendedor


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_emprendedor(
    emprendedor_data: EmprendedorCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo emprendedor
    
    URL final: POST /api/v1/emprendedores
    
    Body (JSON):
    {
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "telefono": "+598 99 123 456",
        "vinculo_institucional": "Estudiante UCU"
    }
    
    Returns:
    - Emprendedor creado con su ID
    """
    nuevo_emprendedor = Emprendedor(**emprendedor_data.model_dump())
    db.add(nuevo_emprendedor)
    db.commit()
    db.refresh(nuevo_emprendedor)
    return nuevo_emprendedor


@router.put("/{emprendedor_id}", status_code=status.HTTP_200_OK)
def actualizar_emprendedor(
    emprendedor_id: int,
    emprendedor_data: EmprendedorUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un emprendedor existente
    
    URL final: PUT /api/v1/emprendedores/5
    
    Body (JSON) - todos los campos son opcionales:
    {
        "nombre": "Juan Pérez Actualizado",
        "telefono": "+598 99 999 999"
    }
    """
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == emprendedor_id
    ).first()
    
    if not emprendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emprendedor con ID {emprendedor_id} no encontrado"
        )
    
    update_data = emprendedor_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(emprendedor, field, value)
    
    db.commit()
    db.refresh(emprendedor)
    return emprendedor


@router.delete("/{emprendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_emprendedor(
    emprendedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un emprendedor
    
    URL final: DELETE /api/v1/emprendedores/5
    
    Returns:
    - 204 No Content si se eliminó correctamente
    - 404 si no existe
    """
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == emprendedor_id
    ).first()
    
    if not emprendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emprendedor con ID {emprendedor_id} no encontrado"
        )
    
    # Eliminar
    db.delete(emprendedor)
    db.commit()
    
    # 204 no devuelve body
    return None


# ============================================================================
# ENDPOINTS ADICIONALES (EJEMPLOS)
# ============================================================================

@router.get("/{emprendedor_id}/casos")
def obtener_casos_emprendedor(
    emprendedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los casos de un emprendedor específico
    
    URL: GET /api/v1/emprendedores/5/casos
    
    Esto es posible gracias a la relationship en el modelo Emprendedor
    """
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == emprendedor_id
    ).first()
    
    if not emprendedor:
        raise HTTPException(status_code=404, detail="Emprendedor no encontrado")
    
    # Gracias a backref="casos" en el modelo Caso
    return emprendedor.casos


# ============================================================================
# NOTAS PARA TUS COMPAÑEROS
# ============================================================================
# 
# Para crear un nuevo archivo de endpoints (ej: casos.py):
# 
# 1. Copiar este archivo como template
# 2. Cambiar:
#    - Nombre del modelo (Emprendedor → Caso)
#    - Nombre de las variables
#    - Schemas correspondientes
# 3. Importar el router en app/api/v1/api.py
# 4. Incluirlo con api_router.include_router()
# 5. ¡Listo! Los endpoints estarán disponibles
#
# Estructura URL final:
#   /api/v1/{prefix}/{ruta del router}
#   
# Ejemplo:
#   - Prefijo en api.py: "/casos"
#   - Ruta en router: "/"
#   - URL final: /api/v1/casos/
