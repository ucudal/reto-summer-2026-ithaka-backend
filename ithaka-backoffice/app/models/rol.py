"""
Modelo ROL
----------
Representa la tabla 'rol' en PostgreSQL.
Esta tabla guarda los diferentes roles de usuario (ej: admin, tutor, etc.)
"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Rol(Base):
    """
    Clase que representa un rol de usuario en el sistema
    
    Ejemplo de uso:
        rol_admin = Rol(nombre_rol="admin")
        db.add(rol_admin)
        db.commit()
    """
    
    # __tablename__ le dice a SQLAlchemy el nombre EXACTO de la tabla en PostgreSQL
    __tablename__ = "rol"
    
    # PRIMARY KEY - El identificador único de cada rol
    # Integer = tipo de dato entero
    # primary_key=True = es la clave primaria
    # index=True = crea un índice para búsquedas rápidas
    id_rol = Column(Integer, primary_key=True, index=True)
    
    # Nombre del rol (ej: "admin", "tutor", "coordinador")
    # String(50) = máximo 50 caracteres
    # unique=True = no puede haber dos roles con el mismo nombre
    # nullable=False = este campo es obligatorio (NOT NULL en SQL)
    nombre_rol = Column(String(50), unique=True, nullable=False)
    
    # Nota: SERIAL en PostgreSQL se maneja automáticamente.
    # No necesitas hacer nada especial, SQLAlchemy genera IDs automáticamente.
