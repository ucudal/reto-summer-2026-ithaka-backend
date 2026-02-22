from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Caso
from app.models import CatalogoEstados
from app.models import Convocatoria
from app.models.usuario import Usuario
from app.models.asignacion import Asignacion
from app.schemas.caso import CasoCreate, CasoUpdate, CasoResponse
from app.models.programa import Programa
from app.models.apoyo import Apoyo
from app.core.security import get_current_user, require_role
from app.services.auditoria_service import registrar_auditoria_caso
from app.models.asignacion import Asignacion
from app.models.emprendedor import Emprendedor

router = APIRouter()


# ============================================================================
# LISTAR TODOS (GET /)
# ============================================================================
@router.get("/")
def listar_casos(
    skip: int = 0,
    limit: int = 100,
    id_estado: int = None,
    tipo_caso: str = None,
    nombre_estado: str = None,
    id_emprendedor: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """
    Listar todos los casos
    
    URL: GET /api/v1/caso?skip=0&limit=100
    """
    query = db.query(Caso)

    # Si es Tutor, filtrar solo casos asignados
    if current_user.rol.nombre_rol == "Tutor":
        query = query.join(Asignacion).filter(
            Asignacion.id_usuario == current_user.id_usuario
        )

    if tipo_caso:
        query = query.join(CatalogoEstados).filter(CatalogoEstados.tipo_caso == tipo_caso)
    if nombre_estado:
        query = query.join(CatalogoEstados).filter(CatalogoEstados.nombre_estado == nombre_estado)
    if id_emprendedor:
        query = query.filter(Caso.id_emprendedor == id_emprendedor)
    if id_estado:
        query = query.filter(Caso.id_estado == id_estado)
    
    casos = query.offset(skip).limit(limit).all()
    
    # Transformar cada caso para devolver nombres en lugar de IDs
    casos_transformados = []
    for caso in casos:
        id_estado = caso.id_estado
        id_emprendedor = caso.id_emprendedor
        id_convocatoria = caso.id_convocatoria
        id_caso = caso.id_caso
        
        # Obtener nombre del estado
        estado_nombre = None
        if id_estado:
            estado = db.query(CatalogoEstados).filter(CatalogoEstados.id_estado == id_estado).first()
            estado_nombre = estado.nombre_estado if estado else None
        
        # Obtener nombre del emprendedor
        emprendedor_nombre = None
        if id_emprendedor:
            emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == id_emprendedor).first()
            emprendedor_nombre = f"{emprendedor.nombre} {emprendedor.apellido}" if emprendedor else None
        
        # Obtener nombre de la convocatoria
        convocatoria_nombre = None
        if id_convocatoria:
            convocatoria = db.query(Convocatoria).filter(Convocatoria.id_convocatoria == id_convocatoria).first()
            convocatoria_nombre = convocatoria.nombre if convocatoria else None
        
        asignacion = db.query(Asignacion).filter(Asignacion.id_caso == id_caso).first()
        tutor = "Sin asignar"
        
        if asignacion:
            tutor = db.query(Usuario).filter(Usuario.id_usuario == asignacion.id_tutor).first()
            tutor = f"{tutor.nombre} {tutor.apellido}" if tutor else None
        
        # Armar el dict personalizado
        custom_caso = {
            "id_caso": caso.id_caso,
            "nombre_caso": caso.nombre_caso,
            "descripcion": caso.descripcion,
            "fecha_creacion": caso.fecha_creacion,
            "estado": estado_nombre,
            "emprendedor": emprendedor_nombre,
            "convocatoria": convocatoria_nombre,
            "consentimiento_datos": caso.consentimiento_datos,
            "datos_chatbot": caso.datos_chatbot, 
            "tutor": tutor
        }
        casos_transformados.append(custom_caso)
    
    return {"casos": casos_transformados}


# ============================================================================
# OBTENER UNO (GET /{id})
# ============================================================================
@router.get("/{caso_id}")
def obtener_caso(
    caso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """
    Obtener un caso específico por ID
    
    Permisos:
    - Admin: Puede ver cualquier caso
    - Coordinador: Puede ver cualquier caso
    - Tutor: Solo puede ver casos asignados a él
    
    URL: GET /api/v1/casos/5
    """
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    
    if not caso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caso {caso_id} no encontrado"
        )
        
    id_estado = caso.id_estado if caso else None
    id_emprendedor = caso.id_emprendedor if caso else None
    id_convocatoria = caso.id_convocatoria if caso else None
    
    # Si es Tutor, verificar que esté asignado al caso
    if current_user.rol.nombre_rol == "Tutor":
        asignacion = db.query(Asignacion).filter(
            Asignacion.id_caso == caso_id,
            Asignacion.id_usuario == current_user.id_usuario
        ).first()
        
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este caso"
            )
    
    return caso

    if id_estado:
        estado = db.query(CatalogoEstados).filter(CatalogoEstados.id_estado == id_estado).first()
        caso.id_estado = estado.nombre_estado if estado else None
    
    if id_emprendedor:
        emprendedor = db.query(Usuario).filter(Usuario.id_usuario == id_emprendedor).first()
        caso.id_emprendedor = f"{emprendedor.nombre} {emprendedor.apellido}" if emprendedor else None   
    
    if id_convocatoria:
        convocatoria = db.query(Convocatoria).filter(Convocatoria.id_convocatoria == id_convocatoria).first()
        caso.id_convocatoria = convocatoria.nombre if convocatoria else None
    
    apoyo = db.query(Apoyo).filter(Apoyo.id_caso == caso_id).first()
    
    if apoyo:
        programa = db.query(Programa).filter(Programa.id_programa == apoyo.id_programa).first()
        if programa:
            apoyo = programa.nombre  
    else:
        apoyo = "Sin apoyo asignado"     
    
    custom_case = {"fecha_creacion": caso.fecha_creacion, "id_caso": caso.id_caso,"descripcion": caso.descripcion, "estado": caso.id_estado, "emprendedor": caso.id_emprendedor, "convocatoria": caso.id_convocatoria, "consentimiento_datos": caso.consentimiento_datos, "nombre_caso": caso.nombre_caso, "datos_chatbot": caso.datos_chatbot, "programa_apoyo": apoyo} # agregar tutor
    
    return custom_case



# ============================================================================
# CREAR (POST /)
# ============================================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_caso(
    caso_data: CasoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Crear un nuevo caso
    
    Permisos:
    - Admin: Puede crear casos
    - Coordinador: Puede crear casos
    - Tutor: NO puede crear casos
    
    URL: POST /api/v1/casos
    
    Body ejemplo:
    {
        "campo1": "valor1",
        "campo2": "valor2"
    }
    """
    nuevo_caso = Caso(**caso_data.model_dump())
    db.add(nuevo_caso)
    db.flush()  # Para obtener el id_caso antes del commit
    
    # Auditoría: Caso creado
    registrar_auditoria_caso(
        db=db,
        accion="Caso creado",
        id_usuario=current_user.id_usuario,
        id_caso=nuevo_caso.id_caso,
        valor_nuevo=f"Caso '{nuevo_caso.nombre_caso}' creado"
    )
    
    db.commit()
    db.refresh(nuevo_caso)
    return nuevo_caso


# ============================================================================
# ACTUALIZAR (PUT /{id})
# ============================================================================
@router.put("/{caso_id}")
def actualizar_caso(
    caso_id: int,
    caso_data: CasoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """
    Actualizar un caso existente
    
    Permisos:
    - Admin: Puede actualizar cualquier caso
    - Coordinador: Puede actualizar cualquier caso
    - Tutor: Solo puede actualizar casos asignados a él
    
    URL: PUT /api/v1/casos/5
    """
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    # Si es Tutor, verificar que esté asignado al caso
    if current_user.rol.nombre_rol == "Tutor":
        asignacion = db.query(Asignacion).filter(
            Asignacion.id_caso == caso_id,
            Asignacion.id_usuario == current_user.id_usuario
        ).first()
        
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este caso"
            )
    
    # Guardar valores anteriores para auditoría
    valores_anteriores = {}
    update_data = caso_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        valores_anteriores[field] = getattr(caso, field)
        setattr(caso, field, value)
    
    # Auditoría: Caso actualizado
    if valores_anteriores:
        registrar_auditoria_caso(
            db=db,
            accion="Caso actualizado",
            id_usuario=current_user.id_usuario,
            id_caso=caso_id,
            valor_anterior=str(valores_anteriores),
            valor_nuevo=str(update_data)
        )
    
    db.commit()
    db.refresh(caso)
    return caso


# # ============================================================================
# # ELIMINAR (DELETE /{id})
# # ============================================================================
# @router.delete("/{caso_id}", status_code=status.HTTP_204_NO_CONTENT)
# def eliminar_caso(
#     caso_id: int,
#     db: Session = Depends(get_db)
#     # current_user: Usuario = Depends(require_role(["admin"]))  # TEMPORALMENTE DESACTIVADO - JWT
# ):
#     """
#     Eliminar un caso
    
#     URL: DELETE /api/v1/casos/5
#     """
#     caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    
#     if not caso:
#         raise HTTPException(status_code=404, detail="Caso no encontrado")
    
#     # Auditoría: Caso eliminado
#     # TODO: Cuando se active JWT, usar current_user.id_usuario
#     registrar_auditoria_caso(
#         db=db,
#         accion="Caso eliminado",
#         id_usuario=1,  # TEMPORAL: Reemplazar con current_user.id_usuario
#         id_caso=caso_id,
#         valor_anterior=f"Caso '{caso.nombre_caso}' (ID: {caso_id})"
#     )
    
#     db.delete(caso)
#     db.commit()
#     return None



@router.put("/{caso_id}/cambiar_estado")
def cambiar_estado_caso(
    caso_id: int,
    nombre_estado: str,  # "En Revisión", "Aprobado", etc
    tipo_caso: str,      # "Postulacion" o "Proyecto"
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    """
    Cambiar el estado de un caso
    
    Permisos:
    - Admin: Puede cambiar estado de cualquier caso
    - Coordinador: Puede cambiar estado de cualquier caso
    - Tutor: NO puede cambiar estados
    
    URL: PUT /api/v1/casos/5/cambiar_estado?nombre_estado=Aprobado&tipo_caso=Proyecto
    """
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    # Obtener estado anterior para auditoría
    estado_anterior = db.query(CatalogoEstados).filter(
        CatalogoEstados.id_estado == caso.id_estado
    ).first()
    
    estado_catalogo = db.query(CatalogoEstados).filter(
        CatalogoEstados.nombre_estado == nombre_estado,
        CatalogoEstados.tipo_caso == tipo_caso
    ).first()
    
    if not estado_catalogo:
        raise HTTPException(
            status_code=404, 
            detail=f"Estado '{nombre_estado}' no existe para tipo '{tipo_caso}'"
        )
    
    caso.id_estado = estado_catalogo.id_estado
    
    # Auditoría: Cambio de estado (CRÍTICO)
    registrar_auditoria_caso(
        db=db,
        accion="Cambio de estado",
        id_usuario=current_user.id_usuario,
        id_caso=caso_id,
        valor_anterior=f"{estado_anterior.nombre_estado} ({estado_anterior.tipo_caso})" if estado_anterior else None,
        valor_nuevo=f"{nombre_estado} ({tipo_caso})"
    )
    
    db.commit()
    db.refresh(caso)
    
    return caso



