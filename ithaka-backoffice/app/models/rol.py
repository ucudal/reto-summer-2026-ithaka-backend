"""
Modelo ROL
----------
Representa los roles de usuario en el sistema (admin, usuario, etc.)

Tabla: rol
Columnas según SQL:
- id_rol SERIAL PRIMARY KEY
- nombre_rol VARCHAR(50) NOT NULL UNIQUE
- descripcion TEXT
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Rol(Base):
    __tablename__ = "rol"
    
    # Columnas
    id_rol = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_rol = Column(String(50), nullable=False, unique=True)
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")
