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

# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.db.database import Base
# 
# class Auditoria(Base):
#     __tablename__ = "auditoria"
#     # ... agregar columnas
