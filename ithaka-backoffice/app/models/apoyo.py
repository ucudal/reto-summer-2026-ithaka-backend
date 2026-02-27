"""
Modelo APOYO
------------
TODO: Implementar usando TEMPLATE.py como guía

Tabla: apoyo
Columnas según SQL:
- id_apoyo SERIAL PRIMARY KEY
- tipo_apoyo VARCHAR(150) NOT NULL
- fecha_inicio DATE
- fecha_fin DATE
- id_caso INTEGER NOT NULL (FK a caso)
- id_programa INTEGER NOT NULL (FK a programa)
"""
from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.db.database import Base


class Apoyo(Base):
    __tablename__ = "apoyo"

    id_apoyo = Column(Integer, primary_key=True, index=True)
    tipo_apoyo = Column(String(150), nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    id_caso = Column(Integer, ForeignKey("caso.id_caso"), nullable=False)
    id_programa = Column(Integer, ForeignKey("programa.id_programa"), nullable=False)
