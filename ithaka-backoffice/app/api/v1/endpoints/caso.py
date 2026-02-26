from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db
from app.models import Caso, CatalogoEstados, Convocatoria, Apoyo, Programa
from app.models.usuario import Usuario
from app.models.asignacion import Asignacion
from app.models.emprendedor import Emprendedor
from app.schemas.caso import CasoCreate, CasoUpdate, CasoResponse
from app.core.security import require_role
from app.services.auditoria_service import registrar_auditoria_caso
from app.services.export_service import ExportService
from sqlalchemy.exc import IntegrityError

router = APIRouter()


# ============================================================================
# LISTAR TODOS (GET /)
# ============================================================================
@router.get("/", response_model=List[CasoResponse])
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
    query = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    )

    # Restricción por rol Tutor
    if current_user.rol.nombre_rol == "Tutor":
        query = query.join(Asignacion).filter(
            Asignacion.id_usuario == current_user.id_usuario
        )

    # Filtros
    if id_estado:
        query = query.filter(Caso.id_estado == id_estado)

    if id_emprendedor:
        query = query.filter(Caso.id_emprendedor == id_emprendedor)

    if id_convocatoria:
        query = query.filter(Caso.id_convocatoria == id_convocatoria)

    if id_tutor:
        query = query.join(Asignacion).filter(Asignacion.id_usuario == id_tutor)

    if tipo_caso:
        query = query.join(Caso.estado).filter(CatalogoEstados.tipo_caso == tipo_caso)

    if nombre_estado:
        query = query.join(Caso.estado).filter(CatalogoEstados.nombre_estado == nombre_estado)

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

        id_asignacion = "Sin Asignar"
        id_usuario_tutor = "Sin Asignar"
        asignacion = db.query(Asignacion).filter(Asignacion.id_caso == id_caso).first()
        if asignacion:
            id_asignacion = asignacion.id_asignacion
            id_usuario_tutor = asignacion.id_usuario
        tutor = "Sin asignar"
        tutor_nombre = "Sin asignar"
        if asignacion:
            tutor = db.query(Usuario).filter(Usuario.id_usuario == asignacion.id_usuario).first()
            tutor_nombre = f"{tutor.nombre} {tutor.apellido}" if tutor else None


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
            "tutor_nombre": tutor_nombre,
            "id_tutor": id_usuario_tutor,
            "asignacion": id_asignacion
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
@router.get("/{caso_id}", response_model=CasoResponse)
def obtener_caso(
    caso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    caso = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    ).filter(Caso.id_caso == caso_id).first()

    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    if current_user.rol.nombre_rol == "Tutor":
        if not any(asig.id_usuario == current_user.id_usuario for asig in caso.asignaciones):
            raise HTTPException(status_code=403, detail="No tienes acceso a este caso")

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
    id_asignacion = "Sin Asignar"
    id_usuario_tutor = "Sin Asignar"

    asignacion = db.query(Asignacion).filter(Asignacion.id_caso == caso_id).first()
    if asignacion:
        id_asignacion = asignacion.id_asignacion
        id_usuario_tutor = asignacion.id_usuario
    tutor = "Sin asignar"
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
        "tutor": tutor_nombre,
        "id_tutor": id_usuario_tutor,
        "asignacion": id_asignacion
    }
    return custom_case

    return caso


# ============================================================================
# CREAR
# ============================================================================
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CasoResponse)
def crear_caso(
    caso_data: CasoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    estado_postulado = db.query(CatalogoEstados).filter(
        func.lower(CatalogoEstados.nombre_estado) == "postulado",
        func.lower(CatalogoEstados.tipo_caso) == "postulacion"
    ).first()

    if not estado_postulado:
        raise HTTPException(status_code=500, detail="No existe el estado 'Postulado'.")

    nuevo_caso = Caso(
        **caso_data.model_dump(exclude={"id_estado"}),
        id_estado=estado_postulado.id_estado
    )

    db.add(nuevo_caso)
    try:
        db.flush()
    except IntegrityError as e:
        db.rollback()
        # Detectar error de clave foránea
        if 'foreign key constraint' in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="ID de emprendedor, convocatoria o estado inválido. Verifica que existan.")
        raise HTTPException(status_code=400, detail=str(e.orig))

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
# ACTUALIZAR
# ============================================================================
@router.put("/{caso_id}", response_model=CasoResponse)
def actualizar_caso(
    caso_id: int,
    caso_data: CasoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()

    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    if current_user.rol.nombre_rol == "Tutor":
        if not any(asig.id_usuario == current_user.id_usuario for asig in caso.asignaciones):
            raise HTTPException(status_code=403, detail="No tienes acceso a este caso")

    update_data = caso_data.model_dump(exclude_unset=True)
    valores_anteriores = {k: getattr(caso, k) for k in update_data}

    for field, value in update_data.items():
        setattr(caso, field, value)

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