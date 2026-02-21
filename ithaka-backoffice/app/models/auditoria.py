"""
Modelo AUDITORIA
----------------
TODO: Implementar usando TEMPLATE.py como guía

Tabla: auditoria
Columnas según SQL:
- id_auditoria SERIAL PRIMARY KEY
- timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- accion VARCHAR(150) NOT NULL
- valor_anterior TEXT
- valor_nuevo TEXT
- id_usuario INTEGER NOT NULL (FK a usuario)
- id_caso INTEGER NOT NULL (FK a caso)
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.database import Base


class Auditoria(Base):
    __tablename__ = "auditoria"

    id_auditoria = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    accion = Column(String(150), nullable=False)
    valor_anterior = Column(Text)
    valor_nuevo = Column(Text)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_caso = Column(Integer, ForeignKey("caso.id_caso"), nullable=True)
