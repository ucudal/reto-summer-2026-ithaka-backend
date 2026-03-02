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
    """
    Transforma una instancia del modelo Caso en un diccionario
    con el formato esperado por el schema CasoResponse.

    Se encarga de:
    - Resolver relaciones (estado, emprendedor, convocatoria, tutor).
    - Manejar valores nulos.
    - Normalizar nombres y campos derivados.
    """
    estado = caso.estado
    emprendedor = caso.emprendedor
    convocatoria = caso.convocatoria

    # Se asume que un caso puede tener varias asignaciones,
    # pero solo se toma la primera como referencia principal.
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
    """
    Lista casos con filtros opcionales.
    
    Permite filtrar por:
    - Estado
    - Tipo de caso
    - Nombre del estado
    - Emprendedor
    - Convocatoria
    - Tutor

    Aplica control de acceso:
    - Si el usuario es Tutor, solo puede ver sus propios casos.
    """

    # Se usan joinedload para evitar problemas N+1 en relaciones.
    query = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    )

    # Restricción automática para Tutor
    if current_user.rol.nombre_rol == "Tutor":
        query = query.join(Caso.asignaciones).filter(
            Asignacion.id_usuario == current_user.id_usuario
        )

    # Filtros dinámicos
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
        # Se hace comparación case-insensitive
        query = query.join(Caso.estado).filter(
            func.lower(CatalogoEstados.tipo_caso) == tipo_caso.lower()
        )

    if nombre_estado:
        query = query.join(Caso.estado).filter(
            func.lower(CatalogoEstados.nombre_estado) == nombre_estado.lower()
        )

    # Paginación
    casos = query.offset(skip).limit(limit).all()

    # Serialización manual
    casos_transformados = []
    for caso in casos:
        casos_transformados.append(_serializar_caso_para_response(caso))

    return casos_transformados


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
    """
    Exporta los casos a CSV.
    
    Si con_tutores=True:
        Incluye información detallada de tutores.
    Caso contrario:
        Exportación básica.
    """

    # Se delega completamente la lógica de generación al ExportService
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

    # Se retorna el archivo como attachment descargable
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
    """
    Obtiene el detalle completo de un caso específico.

    Incluye:
    - Estado
    - Emprendedor
    - Convocatoria
    - Tutor
    - Programa de apoyo asociado (si existe)
    """

    caso = db.query(Caso).options(
        joinedload(Caso.estado),
        joinedload(Caso.emprendedor),
        joinedload(Caso.convocatoria),
        joinedload(Caso.asignaciones).joinedload(Asignacion.usuario)
    ).filter(Caso.id_caso == caso_id).first()

    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    # Restricción de acceso para Tutor
    if current_user.rol.nombre_rol == "Tutor":
        if not any(a.id_usuario == current_user.id_usuario for a in caso.asignaciones):
            raise HTTPException(status_code=403, detail="No tienes acceso a este caso")

    # Se busca si el caso tiene apoyo asignado
    apoyo = db.query(Apoyo).filter(Apoyo.id_caso == caso_id).first()
    programa_nombre = None

    if apoyo:
        programa = db.query(Programa).filter(
            Programa.id_programa == apoyo.id_programa
        ).first()
        programa_nombre = programa.nombre if programa else None
    else:
        programa_nombre = "Sin apoyo asignado"

    # Se construye manualmente la respuesta extendida
    custom_case = {
        "fecha_creacion": caso.fecha_creacion,
        "id_caso": caso.id_caso,
        "descripcion": caso.descripcion,
        "id_estado": caso.id_estado,
        "nombre_estado": caso.estado.nombre_estado if caso.estado else None,
        "tipo_caso": caso.estado.tipo_caso if caso.estado else None,
        "id_emprendedor": caso.id_emprendedor,
        "emprendedor": f"{caso.emprendedor.nombre} {caso.emprendedor.apellido}" if caso.emprendedor else None,
        "convocatoria": caso.convocatoria.nombre if caso.convocatoria else None,
        "nombre_caso": caso.nombre_caso,
        "datos_chatbot": caso.datos_chatbot,
        "programa_apoyo": programa_nombre,
        "tutor": (
            f"{caso.asignaciones[0].usuario.nombre} {caso.asignaciones[0].usuario.apellido}"
            if caso.asignaciones else "Sin asignar"
        ),
        "id_tutor": (
            caso.asignaciones[0].usuario.id_usuario
            if caso.asignaciones else "Sin Asignar"
        ),
        "asignacion": (
            caso.asignaciones[0].id_asignacion
            if caso.asignaciones else "Sin Asignar"
        )
    }

    return custom_case