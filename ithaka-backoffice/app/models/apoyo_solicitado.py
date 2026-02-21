"""
Modelo APOYO_SOLICITADO
-----------------------
Representa las categorías de apoyo solicitadas por un caso.

Tabla: apoyo_solicitado
Columnas según SQL:
- id_apoyo_solicitado SERIAL PRIMARY KEY
- categoria_apoyo VARCHAR(150) NOT NULL
- id_caso INTEGER NOT NULL (FK a caso)
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class ApoyoSolicitado(Base):
    __tablename__ = "apoyo_solicitado"
    
    # Columnas
    id_apoyo_solicitado = Column(Integer, primary_key=True, index=True, autoincrement=True)
    categoria_apoyo = Column(String(150), nullable=False)
    
    # Foreign Keys
    id_caso = Column(Integer, ForeignKey("caso.id_caso"), nullable=False)
