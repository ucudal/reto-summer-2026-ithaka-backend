from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.caso import Caso
from app.models.usuario import Usuario
from app.core.security import require_role 

router = APIRouter()

@router.get("/", summary="Listar métricas de proyectos")
def listar_metricas_proyecto(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    """
    Endpoint para listar métricas básicas de proyectos.
    Devuelve el total de casos y su distribución por estado.
    """
    # Total de casos
    total_casos = db.query(Caso).count()

    # Distribución por estado
    distribucion_estados = (
        db.query(Caso.id_estado, func.count(Caso.id_caso).label("cantidad"))
        .group_by(Caso.id_estado)
        .all()
    )

    return {
        "total_casos": total_casos,
        "distribucion_estados": [
            {"id_estado": estado.id_estado, "cantidad": estado.cantidad}
            for estado in distribucion_estados
        ],
    }