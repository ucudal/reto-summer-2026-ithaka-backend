"""
Modelo USUARIO
--------------
Representa los usuarios del sistema con autenticación y roles

Tabla: usuario
Columnas según SQL:
- id_usuario SERIAL PRIMARY KEY
- nombre VARCHAR(150) NOT NULL
- apellido VARCHAR(150)
- email VARCHAR(150) NOT NULL UNIQUE
- password_hash TEXT NOT NULL
- activo BOOLEAN DEFAULT TRUE
- id_rol INTEGER NOT NULL (FK a rol)
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Usuario(Base):
    __tablename__ = "usuario"
    
    # Columnas
    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    apellido = Column(String(150), nullable=True)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(Text, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    
    # Foreign Keys
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    
    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    # Otras relaciones se agregarán cuando se implementen esos modelos:
    # asignaciones = relationship("Asignacion", back_populates="usuario")
    # notas = relationship("Nota", back_populates="usuario")
