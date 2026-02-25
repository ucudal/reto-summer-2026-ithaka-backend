from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Caso, CatalogoEstados
from app.models import Convocatoria
from app.models.usuario import Usuario
from app.models.asignacion import Asignacion
from app.schemas.caso import CasoCreate, CasoUpdate, CasoResponse
from app.models.programa import Programa
from app.models.apoyo import Apoyo
from app.core.security import get_current_user, require_role
from app.services.auditoria_service import registrar_auditoria_caso
from app.models.emprendedor import Emprendedor
from app.services.export_service import ExportService

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
    id_convocatoria: int = None,
    id_tutor: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    query = ExportService.construir_query_casos(
        db=db,
        current_user=current_user,
        id_estado=id_estado,
        tipo_caso=tipo_caso,
        nombre_estado=nombre_estado,
        id_emprendedor=id_emprendedor,
        id_convocatoria=id_convocatoria,
        id_tutor=id_tutor
    )
    casos = query.offset(skip).limit(limit).all()
    
    # Transformar cada caso para devolver nombres en lugar de IDs
    casos_transformados = []
    for caso in casos:
        id_estado = caso.id_estado
        id_emprendedor = caso.id_emprendedor
        id_convocatoria = caso.id_convocatoria
        id_caso = caso.id_caso

        # Obtener nombre del estado y tipo_caso
        estado_nombre = None
        tipo_caso_val = None
        if id_estado:
            estado = db.query(CatalogoEstados).filter(CatalogoEstados.id_estado == id_estado).first()
            if estado:
                estado_nombre = estado.nombre_estado
                tipo_caso_val = estado.tipo_caso

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
            tutor = db.query(Usuario).filter(Usuario.id_usuario == asignacion.id_usuario).first()
            tutor = f"{tutor.nombre} {tutor.apellido}" if tutor else None

        # Armar el dict personalizado
        custom_caso = {
            "id_caso": caso.id_caso,
            "nombre_caso": caso.nombre_caso,
            "descripcion": caso.descripcion,
            "fecha_creacion": caso.fecha_creacion,
            "id_estado": caso.id_estado,
            "nombre_estado": estado_nombre,
            "tipo_caso": tipo_caso_val,
            "emprendedor": emprendedor_nombre,
            "convocatoria": convocatoria_nombre,
            "datos_chatbot": caso.datos_chatbot,
            "tutor": tutor
        }
        casos_transformados.append(custom_caso)
    
    return casos_transformados


# ============================================================================
# EXPORTAR (GET /export)
# ============================================================================
@router.get("/export", status_code=status.HTTP_200_OK)
def exportar_casos(
    id_estado: int = None,
    tipo_caso: str = None,
    nombre_estado: str = None,
    id_emprendedor: int = None,
    id_convocatoria: int = None,
    id_tutor: int = None,
    con_tutores: bool = False,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    if con_tutores:
        csv_file = ExportService.exportar_casos_con_tutores_csv(
            db=db,
            current_user=current_user,
            id_estado=id_estado,
            tipo_caso=tipo_caso,
            nombre_estado=nombre_estado,
            id_emprendedor=id_emprendedor,
            id_convocatoria=id_convocatoria,
            id_tutor=id_tutor
        )
        nombre_archivo = ExportService.generar_nombre_archivo("casos_con_tutores")
    else:
        csv_file = ExportService.exportar_casos_csv(
            db=db,
            current_user=current_user,
            id_estado=id_estado,
            tipo_caso=tipo_caso,
            nombre_estado=nombre_estado,
            id_emprendedor=id_emprendedor,
            id_convocatoria=id_convocatoria,
            id_tutor=id_tutor
        )
        nombre_archivo = ExportService.generar_nombre_archivo("casos")

    return Response(
        content=csv_file.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'}
    )


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

    nombre_estado = None
    tipo_caso = None
    if id_estado:
        estado = db.query(CatalogoEstados).filter(CatalogoEstados.id_estado == id_estado).first()
        if estado:
            nombre_estado = estado.nombre_estado
            tipo_caso = estado.tipo_caso
    
    
    if id_emprendedor:
        emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == id_emprendedor).first()
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
    
    # Obtener tutor asignado
    asignacion = db.query(Asignacion).filter(Asignacion.id_caso == caso_id).first()
    tutor_nombre = "Sin asignar"
    if asignacion:
        tutor = db.query(Usuario).filter(Usuario.id_usuario == asignacion.id_usuario).first()
        tutor_nombre = f"{tutor.nombre} {tutor.apellido}" if tutor else None

    custom_case = {
        "fecha_creacion": caso.fecha_creacion,
        "id_caso": caso.id_caso,
        "descripcion": caso.descripcion,
        "id_estado": caso.id_estado,
        "nombre_estado": nombre_estado,
        "tipo_caso": tipo_caso,
        "emprendedor": caso.id_emprendedor,
        "convocatoria": caso.id_convocatoria,
        "nombre_caso": caso.nombre_caso,
        "datos_chatbot": caso.datos_chatbot,
        "programa_apoyo": apoyo,
        "tutor": tutor_nombre
    }
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

    Comportamiento:
    - El estado se fuerza siempre a "Postulado" (tipo Postulacion),
      ignorando cualquier id_estado enviado en el payload.

    URL: POST /api/v1/casos
    """

    estado_postulado = db.query(CatalogoEstados).filter(
        func.lower(CatalogoEstados.nombre_estado) == "postulado",
        func.lower(CatalogoEstados.tipo_caso) == "postulacion"
    ).first()

    if not estado_postulado:
        estado_postulado = db.query(CatalogoEstados).filter(
            func.lower(CatalogoEstados.nombre_estado) == "postulado"
        ).first()

    if not estado_postulado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No existe el estado por defecto 'Postulado'. Configura catalogo_estados."
        )

    nuevo_caso = Caso(
        **caso_data.model_dump(exclude={"id_estado"}),
        id_estado=estado_postulado.id_estado
    )


    if caso_data.id_emprendedor:
        emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == caso_data.id_emprendedor).first()
        if not emprendedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Emprendedor con ID {caso_data.id_emprendedor} no encontrado"
            )

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
