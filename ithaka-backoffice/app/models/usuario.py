"""
Modelo USUARIO
--------------
TODO: Implementar usando TEMPLATE.py como guía

Tabla: usuario
Columnas según SQL:
- id_usuario SERIAL PRIMARY KEY
- nombre VARCHAR(150) NOT NULL
- email VARCHAR(150) NOT NULL UNIQUE
- password_hash TEXT NOT NULL
- activo BOOLEAN DEFAULT TRUE
- id_rol INTEGER NOT NULL (FK a rol)
"""

# from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.database import Base
# 
# class Usuario(Base):
#     __tablename__ = "usuario"
#     # ... agregar columnas
