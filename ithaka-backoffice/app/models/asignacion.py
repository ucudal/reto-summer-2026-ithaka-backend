"""
Modelo ASIGNACION
-----------------
Representa las asignaciones de usuarios (coordinadores/tutores) a casos.

Tabla: asignacion
Columnas según SQL:
- id_asignacion SERIAL PRIMARY KEY
- fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- id_usuario INTEGER NOT NULL (FK a usuario)
- id_caso INTEGER NOT NULL (FK a caso)
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class Asignacion(Base):
    __tablename__ = "asignacion"
    
    # Columnas
    id_asignacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Foreign Keys
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_caso = Column(Integer, ForeignKey("caso.id_caso"), nullable=False)
