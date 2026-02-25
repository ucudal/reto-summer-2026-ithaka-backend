from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.api.deps import get_db
from app.models.caso import Caso
from app.models.catalogo_estados import CatalogoEstados

from app.schemas.metrics import (
    MetricsDashboardResponse,
    EstadoDistribucion,
    EstadoTiempoPromedio,
)

router = APIRouter()

POSTULACION_ORDER = ["Postulado", "En Revisión", "Evaluación", "Rechazado", "Aprobada"]
PROYECTO_ORDER = ["Recibida", "En evaluacion", "Incubado", "Proyecto activo", "Cerrado"]


@router.get("/dashboard", response_model=MetricsDashboardResponse)
def dashboard_metricas(
    tipo_caso: Optional[str] = None,
    id_convocatoria: Optional[int] = None,
    db: Session = Depends(get_db),
):
    base = (
        db.query(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
    )

    if tipo_caso:
        base = base.filter(CatalogoEstados.tipo_caso == tipo_caso)
    if id_convocatoria:
        base = base.filter(Caso.id_convocatoria == id_convocatoria)

    total = base.count()

    if total == 0:
        return {
            "filtros": {"tipo_caso": tipo_caso, "id_convocatoria": id_convocatoria},
            "total_casos": 0,
            "distribucion_por_estado": [],
            "tiempo_promedio_global_dias": None,
            "tiempos_promedio_por_estado": [],
        }

    # Orden especial según el tipo
    if tipo_caso == "Postulacion":
        order_map = {name: idx for idx, name in enumerate(POSTULACION_ORDER)}
        order_expr = case(order_map, value=CatalogoEstados.nombre_estado, else_=999)
    elif tipo_caso == "Proyecto":
        order_map = {name: idx for idx, name in enumerate(PROYECTO_ORDER)}
        order_expr = case(order_map, value=CatalogoEstados.nombre_estado, else_=999)
    else:
        order_expr = CatalogoEstados.id_estado.asc()

    # -----------------------------
    # Distribución por estado
    # -----------------------------
    q_dist = (
        db.query(
            CatalogoEstados.id_estado.label("id_estado"),
            CatalogoEstados.nombre_estado.label("nombre_estado"),
            func.count(Caso.id_caso).label("cantidad"),
        )
        .select_from(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
    )

    if tipo_caso:
        q_dist = q_dist.filter(CatalogoEstados.tipo_caso == tipo_caso)
    if id_convocatoria:
        q_dist = q_dist.filter(Caso.id_convocatoria == id_convocatoria)

    q_dist = (
        q_dist.group_by(CatalogoEstados.id_estado, CatalogoEstados.nombre_estado)
              .order_by(order_expr)
              .all()
    )

    distribucion: List[EstadoDistribucion] = []
    for r in q_dist:
        distribucion.append(
            EstadoDistribucion(
                id_estado=r.id_estado,
                nombre_estado=r.nombre_estado,
                cantidad=r.cantidad,
                porcentaje=round((r.cantidad / total) * 100.0, 2),
            )
        )

    # -----------------------------
    # Tiempos promedio (edad desde creación)
    # -----------------------------
    edad_dias = func.extract("epoch", func.now() - Caso.fecha_creacion) / 86400.0

    q_global = (
        db.query(func.avg(edad_dias))
        .select_from(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
    )
    if tipo_caso:
        q_global = q_global.filter(CatalogoEstados.tipo_caso == tipo_caso)
    if id_convocatoria:
        q_global = q_global.filter(Caso.id_convocatoria == id_convocatoria)

    avg_global = float(q_global.scalar() or 0.0)

    q_estado = (
        db.query(
            CatalogoEstados.id_estado.label("id_estado"),
            CatalogoEstados.nombre_estado.label("nombre_estado"),
            func.avg(edad_dias).label("promedio_dias"),
        )
        .select_from(Caso)
        .join(CatalogoEstados, Caso.id_estado == CatalogoEstados.id_estado)
    )
    if tipo_caso:
        q_estado = q_estado.filter(CatalogoEstados.tipo_caso == tipo_caso)
    if id_convocatoria:
        q_estado = q_estado.filter(Caso.id_convocatoria == id_convocatoria)

    q_estado = (
        q_estado.group_by(CatalogoEstados.id_estado, CatalogoEstados.nombre_estado)
               .order_by(order_expr)
               .all()
    )

    tiempos: List[EstadoTiempoPromedio] = [
        EstadoTiempoPromedio(
            id_estado=r.id_estado,
            nombre_estado=r.nombre_estado,
            promedio_dias=round(float(r.promedio_dias or 0.0), 2),
        )
        for r in q_estado
    ]

    return {
        "filtros": {"tipo_caso": tipo_caso, "id_convocatoria": id_convocatoria},
        "total_casos": total,
        "distribucion_por_estado": distribucion,
        "tiempo_promedio_global_dias": round(avg_global, 2),
        "tiempos_promedio_por_estado": tiempos,
    }