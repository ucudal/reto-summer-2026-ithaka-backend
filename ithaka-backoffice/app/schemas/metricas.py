from pydantic import BaseModel
from typing import List, Optional

class EstadoDistribucion(BaseModel):
    id_estado: int
    nombre_estado: str
    cantidad: int
    porcentaje: float

class EstadoTiempoPromedio(BaseModel):
    id_estado: int
    nombre_estado: str
    promedio_dias: float

class ApoyoDistribucion(BaseModel):
    label: str
    cantidad: int

class DashboardMetricasResponse(BaseModel):
    filtros: dict
    total_casos: int

    distribucion_por_estado: List[EstadoDistribucion]

    tiempo_promedio_global_dias: Optional[float]
    tiempos_promedio_por_estado: List[EstadoTiempoPromedio]

    distribucion_apoyos: List[ApoyoDistribucion]