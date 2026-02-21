"""
Endpoints APOYO
---------------
Gestión de apoyos otorgados a casos.

Endpoints:
- GET /api/v1/apoyos - Listar todos
- GET /api/v1/apoyos/{id} - Obtener uno
- GET /api/v1/apoyos/caso/{id_caso} - Listar por caso
- POST /api/v1/apoyos - Crear (con auditoría)
- PUT /api/v1/apoyos/{id} - Actualizar
- DELETE /api/v1/apoyos/{id} - Eliminar
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.apoyo import Apoyo
from app.models.caso import Caso
from app.models.programa import Programa
from app.schemas.apoyo import ApoyoCreate, ApoyoUpdate, ApoyoResponse
from app.services.auditoria_service import registrar_auditoria_caso

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def listar_apoyos(
    skip: int = 0,             
    limit: int = 100,
    id_caso: Optional[int] = None,
    id_programa: Optional[int] = None,
    db: Session = Depends(get_db)  
):
    """
    Listar todos los apoyos otorgados
    
    Filtros opcionales:
    - id_caso: Ver apoyos de un caso específico
    - id_programa: Ver apoyos de un programa específico
    """
    query = db.query(Apoyo)
    
    if id_caso:
        query = query.filter(Apoyo.id_caso == id_caso)
    
    if id_programa:
        query = query.filter(Apoyo.id_programa == id_programa)
    
    apoyos = query.offset(skip).limit(limit).all()
    return apoyos
    

@router.get("/{apoyo_id}", status_code=status.HTTP_200_OK)
def obtener_apoyo(
    apoyo_id: int,  
    db: Session = Depends(get_db)
):
    """Obtener un apoyo específico por ID"""
    apoyo = db.query(Apoyo).filter(
        Apoyo.id_apoyo == apoyo_id
    ).first()
    
    if not apoyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apoyo con ID {apoyo_id} no encontrado"
        )
    
    return apoyo


@router.get("/caso/{id_caso}", response_model=list[ApoyoResponse])
def listar_apoyos_por_caso(
    id_caso: int,
    db: Session = Depends(get_db)
):
    """Listar todos los apoyos otorgados a un caso específico"""
    # Verificar que el caso existe
    caso = db.query(Caso).filter(Caso.id_caso == id_caso).first()
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso con ID {id_caso} no encontrado"
        )
    
    apoyos = db.query(Apoyo).filter(
        Apoyo.id_caso == id_caso
    ).all()
    
    return apoyos

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_apoyo(
    apoyo_data: ApoyoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo apoyo (asignar apoyo a un caso)
    
    Registra auditoría automáticamente.
    """
    # Verificar que el caso existe
    caso = db.query(Caso).filter(
        Caso.id_caso == apoyo_data.id_caso
    ).first()
    
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso con ID {apoyo_data.id_caso} no encontrado"
        )
    
    # Verificar que el programa existe
    programa = db.query(Programa).filter(
        Programa.id_programa == apoyo_data.id_programa
    ).first()
    
    if not programa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Programa con ID {apoyo_data.id_programa} no encontrado"
        )
    
    # Crear el apoyo
    nuevo_apoyo = Apoyo(**apoyo_data.model_dump())
    db.add(nuevo_apoyo)
    
    # Registrar en auditoría
    # TODO: Necesitamos el id_usuario del staff que otorga el apoyo
    # Por ahora usamos el primer usuario del caso asignado
    from app.models.asignacion import Asignacion
    asignacion = db.query(Asignacion).filter(
        Asignacion.id_caso == apoyo_data.id_caso
    ).first()
    
    if asignacion:
        registrar_auditoria_caso(
            db=db,
            accion="Apoyo otorgado",
            id_usuario=asignacion.id_usuario,
            id_caso=apoyo_data.id_caso,
            valor_anterior=None,
            valor_nuevo=f"{apoyo_data.tipo_apoyo} - {programa.nombre}"
        )
    
    db.commit()
    db.refresh(nuevo_apoyo)
    return nuevo_apoyo


@router.put("/{apoyo_id}", status_code=status.HTTP_200_OK)
def actualizar_apoyo(
    apoyo_id: int,
    apoyo_data: ApoyoUpdate,
    db: Session = Depends(get_db)
):
   
    apoyo = db.query(Apoyo).filter(
        Apoyo.id_apoyo == apoyo_id
    ).first()
    
    if not apoyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apoyo con ID {apoyo_id} no encontrado"
        )
    
    for key, value in apoyo_data.model_dump(exclude_unset=True).items():
        setattr(apoyo, key, value)
    
    db.commit()
    db.refresh(apoyo)
    return apoyo

@router.delete("/{apoyo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_apoyo(
    apoyo_id: int,
    db: Session = Depends(get_db)
):
    apoyo = db.query(Apoyo).filter(
        Apoyo.id_apoyo == apoyo_id
    ).first()
    
    if not apoyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apoyo con ID {apoyo_id} no encontrado"
        )
    
    db.delete(apoyo)
    db.commit()
    return