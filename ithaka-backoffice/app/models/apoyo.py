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

# from sqlalchemy import Column, Integer, String, Date, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.database import Base
# 
# class Apoyo(Base):
#     __tablename__ = "apoyo"
#     # ... agregar columnas
