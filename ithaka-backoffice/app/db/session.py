from typing import Generator
from app.db.database import SessionLocal

def get_db() -> Generator:
    """
    Dependency para obtener sesión de base de datos.
    Se usa en los endpoints como: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()