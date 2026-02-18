from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Imports de tu aplicación
from app.api.deps import get_db
from app.models import Emprendedor
from app.schemas.emprendedor import EmprendedorCreate, EmprendedorUpdate, EmprendedorResponse


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def listar_emprendedores(
    skip: int = 0,             
    limit: int = 100,           
    db: Session = Depends(get_db)  
):
   
    emprendedores = db.query(Emprendedor).offset(skip).limit(limit).all()
    
    return emprendedores
 

@router.get("/{emprendedor_id}", status_code=status.HTTP_200_OK)
def obtener_emprendedor(
    emprendedor_id: int,  
    db: Session = Depends(get_db)
):
  
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == emprendedor_id
    ).first()
    
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
   
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == emprendedor_id
    ).first()
    
    if not emprendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emprendedor con ID {emprendedor_id} no encontrado"
        )
    
    db.delete(emprendedor)
    db.commit()
    
    return None


@router.get("/{emprendedor_id}/casos")
def obtener_casos_emprendedor(
    emprendedor_id: int,
    db: Session = Depends(get_db)
):
  
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == emprendedor_id
    ).first()
    
    if not emprendedor:
        raise HTTPException(status_code=404, detail="Emprendedor no encontrado")
    
    return emprendedor.casos


