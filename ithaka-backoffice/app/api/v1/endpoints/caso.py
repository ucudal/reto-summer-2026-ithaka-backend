from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_db
from app.models import Caso, CatalogoEstados, Convocatoria, Apoyo, Programa
from app.models.usuario import Usuario
from app.models.asignacion import Asignacion
from app.models.emprendedor import Emprendedor
from app.schemas.caso import CasoCreate, CasoUpdate, CasoResponse
from app.core.security import require_role
from app.services.auditoria_service import registrar_auditoria_caso
from app.services.export_service import ExportService

router = APIRouter()


def _serializar_caso_para_response(caso: Caso) -> dict:
    """Normaliza un caso al formato esperado por CasoResponse."""
    estado = caso.estado
    emprendedor = caso.emprendedor
    convocatoria = caso.convocatoria
    asignacion = caso.asignaciones[0] if caso.asignaciones else None
    tutor = asignacion.usuario if asignacion else None

    return {
        "id_caso": caso.id_caso,
        "nombre_caso": caso.nombre_caso,
        "descripcion": caso.descripcion,
        "fecha_creacion": caso.fecha_creacion,
        "id_estado": caso.id_estado,
        "nombre_estado": estado.nombre_estado if estado else None,
        "tipo_caso": estado.tipo_caso if estado else None,
        "id_emprendedor": caso.id_emprendedor,
        "id_convocatoria": caso.id_convocatoria,
        "emprendedor": f"{emprendedor.nombre} {emprendedor.apellido}" if emprendedor else None,
        "convocatoria": convocatoria.nombre if convocatoria else None,
        "datos_chatbot": caso.datos_chatbot,
        "tutor_nombre": f"{tutor.nombre} {tutor.apellido}" if tutor else "Sin asignar",
        "id_tutor": tutor.id_usuario if tutor else "Sin Asignar",
        "asignacion": asignacion.id_asignacion if asignacion else "Sin Asignar"
    }


# =============================================================================
# LISTAR TODOS
# =============================================================================
@router.get("/", response_model=List[CasoResponse])
def listar_casos(
    skip: int = 0,
    limit: int = 100,
    id_estado: Optional[int] = None,
    tipo_caso: Optional[str] = None,
    nombre_estado: Optional[str] = None,
    id_emprendedor: Optional[int] = None,
    id_convocatoria: Optional[int] = None,
    id_tutor: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    query = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    )

    if current_user.rol.nombre_rol == "Tutor":
        query = query.join(Caso.asignaciones).filter(
            Asignacion.id_usuario == current_user.id_usuario
        )

    if id_estado:
        query = query.filter(Caso.id_estado == id_estado)

    if id_emprendedor:
        query = query.filter(Caso.id_emprendedor == id_emprendedor)

    if id_convocatoria:
        query = query.filter(Caso.id_convocatoria == id_convocatoria)

    if id_tutor:
        query = query.join(Caso.asignaciones).filter(
            Asignacion.id_usuario == id_tutor
        )

    if tipo_caso:
        query = query.join(Caso.estado).filter(
            CatalogoEstados.tipo_caso == tipo_caso
        )

    if nombre_estado:
        query = query.join(Caso.estado).filter(
            CatalogoEstados.nombre_estado == nombre_estado
        )

    casos = query.offset(skip).limit(limit).all()

    casos_transformados = []

    for caso in casos:
        casos_transformados.append(_serializar_caso_para_response(caso))

    return casos_transformados


## MOVE EXPORTAR CASOS ABOVE OBTENER UNO
# =============================================================================
# EXPORTAR
# =============================================================================
@router.get("/export", status_code=status.HTTP_200_OK)
def exportar_casos(
    id_estado: Optional[int] = None,
    tipo_caso: Optional[str] = None,
    nombre_estado: Optional[str] = None,
    id_emprendedor: Optional[int] = None,
    id_convocatoria: Optional[int] = None,
    id_tutor: Optional[int] = None,
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

# =============================================================================
# OBTENER UNO
# =============================================================================
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
        if not any(a.id_usuario == current_user.id_usuario for a in caso.asignaciones):
            raise HTTPException(status_code=403, detail="No tienes acceso a este caso")

    estado = caso.estado
    emprendedor = caso.emprendedor
    convocatoria = caso.convocatoria
    asignacion = caso.asignaciones[0] if caso.asignaciones else None
    tutor = asignacion.usuario if asignacion else None

    apoyo = db.query(Apoyo).filter(Apoyo.id_caso == caso_id).first()
    programa_nombre = None

    if apoyo:
        programa = db.query(Programa).filter(
            Programa.id_programa == apoyo.id_programa
        ).first()
        programa_nombre = programa.nombre if programa else None
    else:
        programa_nombre = "Sin apoyo asignado"

    custom_case = {
        "fecha_creacion": caso.fecha_creacion,
        "id_caso": caso.id_caso,
        "descripcion": caso.descripcion,
        "id_estado": caso.id_estado,
        "nombre_estado": estado.nombre_estado if estado else None,
        "tipo_caso": estado.tipo_caso if estado else None,
        "id_emprendedor": caso.id_emprendedor,
        "emprendedor": f"{emprendedor.nombre} {emprendedor.apellido}" if emprendedor else None,
        "convocatoria": convocatoria.nombre if convocatoria else None,
        "nombre_caso": caso.nombre_caso,
        "datos_chatbot": caso.datos_chatbot,
        "programa_apoyo": programa_nombre,
        "tutor": f"{tutor.nombre} {tutor.apellido}" if tutor else "Sin asignar",
        "id_tutor": tutor.id_usuario if tutor else "Sin Asignar",
        "asignacion": asignacion.id_asignacion if asignacion else "Sin Asignar"
    }

    return custom_case






# =============================================================================
# CREAR
# =============================================================================
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
        **caso_data.model_dump(),
        id_estado=estado_postulado.id_estado
    )

    db.add(nuevo_caso)

    try:
        db.flush()
    except IntegrityError as e:
        db.rollback()
        if "foreign key" in str(e.orig).lower():
            raise HTTPException(
                status_code=400,
                detail="ID de emprendedor o convocatoria inválido."
            )
        raise HTTPException(status_code=400, detail=str(e.orig))

    registrar_auditoria_caso(
        db=db,
        accion="Caso creado",
        id_usuario=current_user.id_usuario,
        id_caso=nuevo_caso.id_caso,
        valor_nuevo=f"Caso '{nuevo_caso.nombre_caso}' creado"
    )

    db.commit()
    caso_creado = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    ).filter(Caso.id_caso == nuevo_caso.id_caso).first()

    return _serializar_caso_para_response(caso_creado)


# =============================================================================
# ACTUALIZAR
# =============================================================================
@router.put("/{caso_id}", response_model=CasoResponse)
def actualizar_caso(
    caso_id: int,
    caso_data: CasoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    caso = db.query(Caso).options(
        joinedload(Caso.asignaciones)
    ).filter(Caso.id_caso == caso_id).first()

    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    if current_user.rol.nombre_rol == "Tutor":
        if not any(a.id_usuario == current_user.id_usuario for a in caso.asignaciones):
            raise HTTPException(status_code=403, detail="No tienes acceso a este caso")

    update_data = caso_data.model_dump(exclude_unset=True)
    valores_anteriores = {k: getattr(caso, k) for k in update_data}

    for field, value in update_data.items():
        setattr(caso, field, value)

    if update_data:
        registrar_auditoria_caso(
            db=db,
            accion="Caso actualizado",
            id_usuario=current_user.id_usuario,
            id_caso=caso_id,
            valor_anterior=str(valores_anteriores),
            valor_nuevo=str(update_data)
        )

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key" in str(e.orig).lower():
            raise HTTPException(
                status_code=400,
                detail="ID de emprendedor, convocatoria o estado inválido."
            )
        raise HTTPException(status_code=400, detail=str(e.orig))

    caso_actualizado = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    ).filter(Caso.id_caso == caso_id).first()

    return _serializar_caso_para_response(caso_actualizado)
