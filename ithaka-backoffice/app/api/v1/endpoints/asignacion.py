"""
Endpoints ASIGNACION
--------------------
TODO: Implementar usando TEMPLATE.py como guía

Endpoints a crear:
* - GET /api/v1/asignaciones - Listar todas
* - GET /api/v1/asignaciones/{id} - Obtener una
* - POST /api/v1/asignaciones - Crear
* - PUT /api/v1/asignaciones/{id} - Actualizar
* - DELETE /api/v1/asignaciones/{id} - Eliminar
"""

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.api.deps import get_db
# from app.models.asignacion import Asignacion
# from app.schemas.asignacion import AsignacionCreate, AsignacionUpdate, AsignacionResponse
# 
# router = APIRouter()
# 
# @router.get("/")
# def listar_asignaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     # ... implementar
#     pass

@router.get("/", status_code=status.HTTP_200_OK)
def listar_asignaciones(
    skip: int = 0,             
    limit: int = 100,           
    db: Session = Depends(get_db)  
):
   
    asignaciones = db.query(Asignacion).offset(skip).limit(limit).all()
    return asignaciones
    

@router.get("/{asignacion_id}", status_code=status.HTTP_200_OK)
def obtener_asignacion(
    asignacion_id: int,  
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
    
    return asignacion

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_asignacion(
    asignacion_data: AsignacionCreate,
    db: Session = Depends(get_db)
):
   
    nueva_asignacion = Asignacion(**asignacion_data.model_dump())
    db.add(nueva_asignacion)
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
    asignacion = db.query(Asignacion).filter(
        Asignacion.id_asignacion == asignacion_id
    ).first()
    
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignacion con ID {asignacion_id} no encontrado"
        )
    
    db.delete(asignacion)
    db.commit()
    return