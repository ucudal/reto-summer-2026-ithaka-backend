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

# from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.db.database import Base
# 
# class Nota(Base):
#     __tablename__ = "nota"
#     # ... agregar columnas
