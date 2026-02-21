"""
Endpoints ASIGNACION
--------------------
Gestión de asignaciones de staff a casos.

Endpoints:
- GET /api/v1/asignaciones - Listar todas
- GET /api/v1/asignaciones/{id} - Obtener una
- GET /api/v1/asignaciones/caso/{id_caso} - Listar por caso
- GET /api/v1/asignaciones/usuario/{id_usuario} - Listar por usuario
- POST /api/v1/asignaciones - Crear (con auditoría)
- DELETE /api/v1/asignaciones/{id} - Eliminar (con auditoría)
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.asignacion import Asignacion
from app.models.usuario import Usuario
from app.models.caso import Caso
from app.schemas.asignacion import AsignacionCreate, AsignacionUpdate, AsignacionResponse
from app.services.auditoria_service import registrar_auditoria_caso

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def listar_asignaciones(
    skip: int = 0,             
    limit: int = 100,
    id_caso: Optional[int] = None,
    id_usuario: Optional[int] = None,
    db: Session = Depends(get_db)  
):
    """
    Listar todas las asignaciones
    
    Filtros opcionales:
    - id_caso: Ver asignaciones de un caso específico
    - id_usuario: Ver asignaciones de un usuario específico
    """
    query = db.query(Asignacion)
    
    if id_caso:
        query = query.filter(Asignacion.id_caso == id_caso)
    
    if id_usuario:
        query = query.filter(Asignacion.id_usuario == id_usuario)
    
    asignaciones = query.offset(skip).limit(limit).all()
    return asignaciones
    

@router.get("/{asignacion_id}", status_code=status.HTTP_200_OK)
def obtener_asignacion(
    asignacion_id: int,  
    db: Session = Depends(get_db)
):
    """Obtener una asignación específica por ID"""
    asignacion = db.query(Asignacion).filter(
        Asignacion.id_asignacion == asignacion_id
    ).first()
    
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignación con ID {asignacion_id} no encontrada"
        )
    
    return asignacion


@router.get("/caso/{id_caso}", response_model=list[AsignacionResponse])
def listar_asignaciones_por_caso(
    id_caso: int,
    db: Session = Depends(get_db)
):
    """Listar todas las asignaciones de un caso específico"""
    # Verificar que el caso existe
    caso = db.query(Caso).filter(Caso.id_caso == id_caso).first()
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso con ID {id_caso} no encontrado"
        )
    
    asignaciones = db.query(Asignacion).filter(
        Asignacion.id_caso == id_caso
    ).all()
    
    return asignaciones


@router.get("/usuario/{id_usuario}", response_model=list[AsignacionResponse])
def listar_asignaciones_por_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    """Listar todas las asignaciones de un usuario específico"""
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {id_usuario} no encontrado"
        )
    
    asignaciones = db.query(Asignacion).filter(
        Asignacion.id_usuario == id_usuario
    ).all()
    
    return asignaciones

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_asignacion(
    asignacion_data: AsignacionCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva asignación de staff a un caso
    
    Registra auditoría automáticamente.
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == asignacion_data.id_usuario
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {asignacion_data.id_usuario} no encontrado"
        )
    
    # Verificar que el caso existe
    caso = db.query(Caso).filter(
        Caso.id_caso == asignacion_data.id_caso
    ).first()
    
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso con ID {asignacion_data.id_caso} no encontrado"
        )
    
    # Verificar si ya existe una asignación igual
    asignacion_existente = db.query(Asignacion).filter(
        Asignacion.id_usuario == asignacion_data.id_usuario,
        Asignacion.id_caso == asignacion_data.id_caso
    ).first()
    
    if asignacion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario {usuario.nombre} ya está asignado a este caso"
        )
    
    # Crear la asignación
    nueva_asignacion = Asignacion(**asignacion_data.model_dump())
    db.add(nueva_asignacion)
    
    # Registrar en auditoría
    registrar_auditoria_caso(
        db=db,
        accion="Asignación de staff",
        id_usuario=asignacion_data.id_usuario,
        id_caso=asignacion_data.id_caso,
        valor_anterior=None,
        valor_nuevo=usuario.nombre
    )
    
    db.commit()
    db.refresh(nueva_asignacion)
    
    return nueva_asignacion


@router.put("/{asignacion_id}", status_code=status.HTTP_200_OK)
def actualizar_asignacion(
    asignacion_id: int,
    asignacion_data: AsignacionUpdate,
    db: Session = Depends(get_db)
):
   
    asignacion = db.query(Asignacion).filter(
        Asignacion.id_asignacion == asignacion_id
    ).first()
    
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignacion con ID {asignacion_id} no encontrado"
        )
    
    for key, value in asignacion_data.model_dump(exclude_unset=True).items():
        setattr(asignacion, key, value)
    
    db.commit()
    db.refresh(asignacion)
    return asignacion

@router.delete("/{asignacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asignacion(
    asignacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una asignación
    
    Registra auditoría automáticamente.
    """
    asignacion = db.query(Asignacion).filter(
        Asignacion.id_asignacion == asignacion_id
    ).first()
    
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignación con ID {asignacion_id} no encontrada"
        )
    
    # Obtener datos antes de eliminar para auditoría
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == asignacion.id_usuario
    ).first()
    
    # Registrar en auditoría
    registrar_auditoria_caso(
        db=db,
        accion="Eliminación de asignación",
        id_usuario=asignacion.id_usuario,
        id_caso=asignacion.id_caso,
        valor_anterior=usuario.nombre if usuario else None,
        valor_nuevo=None
    )
    
    db.delete(asignacion)
    db.commit()
    
    return None