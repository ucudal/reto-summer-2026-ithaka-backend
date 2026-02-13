"""
Modelo PROGRAMA
---------------
Representa la tabla 'programa' en PostgreSQL.
Almacena los programas de apoyo disponibles (ej: "Incubación", "Aceleración", etc.)
"""

from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class Programa(Base):
    """
    Clase que representa un programa de apoyo
    
    Ejemplo:
        programa = Programa(
            nombre="Programa de Incubación",
            activo=True
        )
    """
    
    __tablename__ = "programa"
    
    # ID único del programa
    id_programa = Column(Integer, primary_key=True, index=True)
    
    # Nombre del programa (ej: "Incubación", "Aceleración", "Mentoría")
    nombre = Column(String(150), nullable=False)
    
    # Indica si el programa está actualmente activo
    # Boolean = verdadero/falso (TRUE/FALSE en PostgreSQL)
    # default=True = si no especificas, será True
    activo = Column(Boolean, default=True)
