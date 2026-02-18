"""
Endpoints APOYO
---------------
TODO: Implementar usando TEMPLATE.py como guía

Endpoints a crear:
* - GET /api/v1/apoyos - Listar todos 
* - GET /api/v1/apoyos/{id} - Obtener uno
* - POST /api/v1/apoyos - Crear
* - PUT /api/v1/apoyos/{id} - Actualizar
* - DELETE /api/v1/apoyos/{id} - Eliminar
"""

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.api.deps import get_db
# from app.models.apoyo import Apoyo
# from app.schemas.apoyo import ApoyoCreate, ApoyoUpdate, ApoyoResponse
# 
# router = APIRouter()
# 
# @router.get("/")
# def listar_apoyos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     # ... implementar
#     pass

@router.get("/", status_code=status.HTTP_200_OK)
def listar_apoyos(
    skip: int = 0,             
    limit: int = 100,           
    db: Session = Depends(get_db)  
):
   
    apoyos = db.query(Apoyo).offset(skip).limit(limit).all()
    return apoyos
    

@router.get("/{apoyo_id}", status_code=status.HTTP_200_OK)
def obtener_apoyo(
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
    
    return apoyo

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_apoyo(
    apoyo_data: ApoyoCreate,
    db: Session = Depends(get_db)
):
   
    nuevo_apoyo = Apoyo(**apoyo_data.model_dump())
    db.add(nuevo_apoyo)
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