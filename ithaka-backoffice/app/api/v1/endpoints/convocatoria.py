from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.convocatoria import Convocatoria
from app.schemas.convocatoria import ConvocatoriaCreate, ConvocatoriaUpdate, ConvocatoriaResponse
from app.services.auditoria_service import registrar_auditoria_general

router = APIRouter()


@router.get("/", response_model=List[ConvocatoriaResponse])
def listar_convocatorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Convocatoria).offset(skip).limit(limit).all()


@router.get("/{convocatoria_id}", response_model=ConvocatoriaResponse)
def obtener_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    convocatoria = (
        db.query(Convocatoria)
        .filter(Convocatoria.id_convocatoria == convocatoria_id)
        .first()
    )
    if not convocatoria:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return convocatoria


@router.post("/", response_model=ConvocatoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_convocatoria(convocatoria_data: ConvocatoriaCreate, db: Session = Depends(get_db)):
    nueva = Convocatoria(**convocatoria_data.model_dump())
    db.add(nueva)
    db.flush()  # Para obtener el id antes del commit
    
    # Auditoría: Convocatoria creada
    # TODO: Cuando se active JWT, usar current_user.id_usuario
    registrar_auditoria_general(
        db=db,
        accion="Convocatoria creada",
        id_usuario=1,  # TEMPORAL: Reemplazar con current_user.id_usuario
        valor_nuevo=f"Convocatoria '{nueva.nombre}' (ID: {nueva.id_convocatoria})"
    )
    
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{convocatoria_id}", response_model=ConvocatoriaResponse)
def actualizar_convocatoria(convocatoria_id: int, convocatoria_data: ConvocatoriaUpdate, db: Session = Depends(get_db)):
    convocatoria = (
        db.query(Convocatoria)
        .filter(Convocatoria.id_convocatoria == convocatoria_id)
        .first()
    )
    if not convocatoria:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")

    # Guardar valores anteriores para auditoría
    valores_anteriores = {}
    update_data = convocatoria_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        valores_anteriores[field] = getattr(convocatoria, field)
        setattr(convocatoria, field, value)

    # Auditoría: Convocatoria actualizada
    if valores_anteriores:
        # TODO: Cuando se active JWT, usar current_user.id_usuario
        registrar_auditoria_general(
            db=db,
            accion="Convocatoria actualizada",
            id_usuario=1,  # TEMPORAL: Reemplazar con current_user.id_usuario
            valor_anterior=str(valores_anteriores),
            valor_nuevo=str(update_data)
        )

    db.commit()
    db.refresh(convocatoria)
    return convocatoria



# ============================================================================
# ELIMINAR (DELETE /{id}) - ENDPOINT DESHABILITADO
# ============================================================================
# Las convocatorias NO se eliminan porque pueden tener casos asociados.
# Eliminarlas rompería la integridad referencial. Si necesita "cerrar"
# una convocatoria, actualice su fecha_cierre.
#
# @router.delete("/{convocatoria_id}", status_code=status.HTTP_204_NO_CONTENT)
# def eliminar_convocatoria(...):
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="No se permite eliminar convocatorias con casos asociados."
#     )

# @router.delete("/{convocatoria_id}", status_code=status.HTTP_204_NO_CONTENT)
# def eliminar_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
#     convocatoria = (
#         db.query(Convocatoria)
#         .filter(Convocatoria.id_convocatoria == convocatoria_id)
#         .first()
#     )
#     if not convocatoria:
#         raise HTTPException(status_code=404, detail="Convocatoria no encontrada")

#     # Auditoría: Convocatoria eliminada
#     # TODO: Cuando se active JWT, usar current_user.id_usuario
#     registrar_auditoria_general(
#         db=db,
#         accion="Convocatoria eliminada",
#         id_usuario=1,  # TEMPORAL: Reemplazar con current_user.id_usuario
#         valor_anterior=f"Convocatoria '{convocatoria.nombre}' (ID: {convocatoria_id})"
#     )

#     db.delete(convocatoria)
#     db.commit()
#     return None

