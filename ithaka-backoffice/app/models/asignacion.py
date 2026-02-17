"""
Modelo ASIGNACION
-----------------
TODO: Implementar usando TEMPLATE.py como guía

Tabla: asignacion
Columnas según SQL:
- id_asignacion SERIAL PRIMARY KEY
- fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- id_usuario INTEGER NOT NULL (FK a usuario)
- id_caso INTEGER NOT NULL (FK a caso)
"""

# from sqlalchemy import Column, Integer, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.db.database import Base
# 
# class Asignacion(Base):
#     __tablename__ = "asignacion"
#     # ... agregar columnas
