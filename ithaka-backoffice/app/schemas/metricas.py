from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class EstadoDistribucion(BaseModel):
    id_estado: int
    nombre_estado: str
    cantidad: int
    porcentaje: float


class ApoyoDistribucion(BaseModel):
    label: str
    cantidad: int


class TotalesDashboard(BaseModel):
    total_postulaciones: int
    total_proyectos: int
    total_proyectos_incubados: int
    total_tutores: int
    total_emprendedores: int
    total_apoyos: int


class DashboardMetricasResponse(BaseModel):
    filtros: Dict[str, Any]
    totales: TotalesDashboard
    proyectos_por_estado: List[EstadoDistribucion]
    postulaciones_por_estado: List[EstadoDistribucion]
    distribucion_apoyos: List[ApoyoDistribucion]