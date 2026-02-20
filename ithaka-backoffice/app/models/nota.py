"""
Modelo NOTA
-----------
TODO: Implementar usando TEMPLATE.py como guía

Tabla: nota
Columnas según SQL:
- id_nota SERIAL PRIMARY KEY
- contenido TEXT NOT NULL
- fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- id_usuario INTEGER NOT NULL (FK a usuario)
- id_caso INTEGER NOT NULL (FK a caso)
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from app.db.database import Base


class Nota(Base):
    __tablename__ = "nota"

    id_nota = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_caso = Column(Integer, ForeignKey("caso.id_caso"), nullable=False)
