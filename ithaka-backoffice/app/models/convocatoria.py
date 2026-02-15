"""
Modelo CONVOCATORIA
-------------------
Representa la tabla 'convocatoria' en PostgreSQL.
Almacena las diferentes convocatorias abiertas para presentar proyectos.
"""

from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


class Convocatoria(Base):
    """
    Clase que representa una convocatoria
    
    Ejemplo:
        convocatoria = Convocatoria(
            nombre="Convocatoria Primavera 2026",
            fecha_cierre=datetime(2026, 3, 31)
        )
    """
    
    __tablename__ = "convocatoria"
    
    # ID único de la convocatoria
    id_convocatoria = Column(Integer, primary_key=True, index=True)
    
    # Nombre de la convocatoria (ej: "Convocatoria 2026-1")
    nombre = Column(String(150), nullable=False)
    
    # Fecha límite para presentar proyectos
    # Es opcional (puede ser None) porque algunas convocatorias pueden ser permanentes
    fecha_cierre = Column(DateTime)
