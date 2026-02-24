from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.caso import Caso´´´´´´´´´´


router = APIRouter()

@router.get("/", )
def listar_metricas_proyecto(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Tutor"]))
):
    metricas = db.query()