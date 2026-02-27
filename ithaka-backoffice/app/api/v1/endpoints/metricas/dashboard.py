from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.api.deps import get_db
from app.models.caso import Caso
from app.models.catalogo_estados import CatalogoEstados
from app.models.apoyo import Apoyo
from app.models.emprendedor import Emprendedor
from app.models.asignacion import Asignacion
from app.models.usuario import Usuario
from app.models.rol import Rol

from app.schemas.metricas import (
    DashboardMetricasResponse,
    EstadoDistribucion,
    ApoyoDistribucion,
    TotalesDashboard,
)

router = APIRouter()

POSTULACION_ORDER = ["Postulado", "En Revisión", "Evaluación", "Rechazado", "Aprobada"]
PROYECTO_ORDER = ["Recibida", "En evaluación", "Incubado", "Proyecto activo", "Cerrado"]


def _order_expr_por_tipo(tipo_caso: Optional[str]):
    if tipo_caso == "Postulacion":
        return case(
            {name: idx for idx, name in enumerate(POSTULACION_ORDER)},
            value=CatalogoEstados.nombre_estado,
            else_=999,
        )
    if tipo_caso == "Proyecto":
        return case(
            {name: idx for idx, name in enumerate(PROYECTO_ORDER)},
            value=CatalogoEstados.nombre_estado,
            else_=999,
        )
    return CatalogoEstados.id_estado.asc()


def _distribucion_por_estado(db: Session, tipo_caso: str, id_convocatoria: Optional[int]) -> List[EstadoDistribucion]:
    order_expr = _order_expr_por_tipo(tipo_caso)

    q = (
        db.query(
            CatalogoEstados.id_estado.label("id_estado"),
            CatalogoEstados.nombre_estado.label("nombre_estado"),
            func.count(Caso.id_caso).label("cantidad"),
        )
        .select_from(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
        .filter(CatalogoEstados.tipo_caso == tipo_caso)
    )

    if id_convocatoria:
        q = q.filter(Caso.id_convocatoria == id_convocatoria)

    rows = (
        q.group_by(CatalogoEstados.id_estado, CatalogoEstados.nombre_estado)
         .order_by(order_expr)
         .all()
    )

    total = sum(r.cantidad for r in rows) or 0

    result: List[EstadoDistribucion] = []
    for r in rows:
        result.append(
            EstadoDistribucion(
                id_estado=r.id_estado,
                nombre_estado=r.nombre_estado,
                cantidad=r.cantidad,
                porcentaje=round((r.cantidad / total) * 100.0, 2) if total else 0.0,
            )
        )
    return result


def _distribucion_apoyos(db: Session, id_convocatoria: Optional[int]) -> List[ApoyoDistribucion]:
    # Distribución por tipo_apoyo (lo que muestra tu gráfico: ValidaLab, Mentoría, etc)
    q = (
        db.query(
            Apoyo.tipo_apoyo.label("label"),
            func.count(Apoyo.id_apoyo).label("cantidad"),
        )
        .select_from(Apoyo)
        .join(Caso, Apoyo.id_caso == Caso.id_caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
        # apoyos se asocian a casos tipo Proyecto (si en tu data también hay apoyos en Postulacion, sacá este filtro)
        .filter(CatalogoEstados.tipo_caso == "Proyecto")
    )

    if id_convocatoria:
        q = q.filter(Caso.id_convocatoria == id_convocatoria)

    rows = (
        q.group_by(Apoyo.tipo_apoyo)
         .order_by(func.count(Apoyo.id_apoyo).desc())
         .all()
    )

    return [ApoyoDistribucion(label=r.label, cantidad=r.cantidad) for r in rows]


@router.get("/dashboard", response_model=DashboardMetricasResponse)
def dashboard_metricas(
    id_convocatoria: Optional[int] = None,
    db: Session = Depends(get_db),
):
    # ============================================================
    # TOTALES (cards)
    # ============================================================

    # total postulaciones = casos cuyo estado es tipo_caso "Postulacion"
    q_post = (
        db.query(func.count(Caso.id_caso))
        .select_from(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
        .filter(CatalogoEstados.tipo_caso == "Postulacion")
    )
    if id_convocatoria:
        q_post = q_post.filter(Caso.id_convocatoria == id_convocatoria)
    total_postulaciones = int(q_post.scalar() or 0)

    # total proyectos = casos cuyo estado es tipo_caso "Proyecto"
    q_proy = (
        db.query(func.count(Caso.id_caso))
        .select_from(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
        .filter(CatalogoEstados.tipo_caso == "Proyecto")
    )
    if id_convocatoria:
        q_proy = q_proy.filter(Caso.id_convocatoria == id_convocatoria)
    total_proyectos = int(q_proy.scalar() or 0)

    # total proyectos incubados = proyectos con estado nombre_estado == "Incubado"
    q_inc = (
        db.query(func.count(Caso.id_caso))
        .select_from(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
        .filter(CatalogoEstados.tipo_caso == "Proyecto")
        .filter(func.lower(CatalogoEstados.nombre_estado) == "incubado")
    )
    if id_convocatoria:
        q_inc = q_inc.filter(Caso.id_convocatoria == id_convocatoria)
    total_proyectos_incubados = int(q_inc.scalar() or 0)

    # total tutores = usuarios con rol "Tutor"
    # (si tu modelo es Usuario -> Rol, esto asume relación usuario.rol.nombre_rol)
    total_tutores = int(
        db.query(func.count(Usuario.id_usuario))
        .join(Rol, Usuario.id_rol == Rol.id_rol)
        .filter(func.lower(Rol.nombre_rol) == "tutor")
        .scalar()
        or 0
    )

    # total emprendedores = cantidad de emprendedores
    total_emprendedores = int(db.query(func.count(Emprendedor.id_emprendedor)).scalar() or 0)

    # total apoyos = cantidad de apoyos
    q_ap = db.query(func.count(Apoyo.id_apoyo)).select_from(Apoyo).join(Caso, Apoyo.id_caso == Caso.id_caso)
    if id_convocatoria:
        q_ap = q_ap.filter(Caso.id_convocatoria == id_convocatoria)
    total_apoyos = int(q_ap.scalar() or 0)

    totales = TotalesDashboard(
        total_postulaciones=total_postulaciones,
        total_proyectos=total_proyectos,
        total_proyectos_incubados=total_proyectos_incubados,
        total_tutores=total_tutores,
        total_emprendedores=total_emprendedores,
        total_apoyos=total_apoyos,
    )

    # ============================================================
    # GRAFICAS
    # ============================================================
    proyectos_por_estado = _distribucion_por_estado(db, "Proyecto", id_convocatoria)
    postulaciones_por_estado = _distribucion_por_estado(db, "Postulacion", id_convocatoria)
    distribucion_apoyos = _distribucion_apoyos(db, id_convocatoria)

    return {
        "filtros": {"id_convocatoria": id_convocatoria},
        "totales": totales,
        "proyectos_por_estado": proyectos_por_estado,
        "postulaciones_por_estado": postulaciones_por_estado,
        "distribucion_apoyos": distribucion_apoyos,
    }