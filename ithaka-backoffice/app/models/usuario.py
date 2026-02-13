"""
Modelo USUARIO
--------------
Representa la tabla 'usuario' en PostgreSQL.
Almacena los usuarios del backoffice (tutores, admins, coordinadores).
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Usuario(Base):
    """
    Clase que representa un usuario del sistema
    
    IMPORTANTE: password_hash NO debe exponerse nunca en las respuestas API
    
    Ejemplo de uso:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"])
        
        usuario = Usuario(
            nombre="Ana García",
            email="ana@ucu.edu.uy",
            password_hash=pwd_context.hash("mi_contraseña_segura"),
            activo=True,
            id_rol=1  # ID del rol "admin" o "tutor"
        )
    """
    
    __tablename__ = "usuario"
    
    # ID único del usuario
    id_usuario = Column(Integer, primary_key=True, index=True)
    
    # Nombre completo
    nombre = Column(String(150), nullable=False)
    
    # Email (único en el sistema)
    email = Column(String(150), unique=True, nullable=False)
    
    # Contraseña hasheada (NUNCA guardes contraseñas en texto plano)
    # Text = tipo de dato para textos largos (el hash es largo)
    password_hash = Column(Text, nullable=False)
    
    # Si el usuario está activo o deshabilitado
    activo = Column(Boolean, default=True)
    
    # ========== FOREIGN KEY ==========
    # Esta columna guarda el ID del rol (apunta a la tabla 'rol')
    # ForeignKey("rol.id_rol") = referencia a la columna id_rol de la tabla rol
    # nullable=False = cada usuario DEBE tener un rol
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    
    # ========== RELATIONSHIP ==========
    # Esto NO es una columna en la base de datos
    # Es una "relación" que SQLAlchemy crea para facilitar el acceso
    # 
    # Con esto puedes hacer:
    #   usuario.rol.nombre_rol  ← Accede directamente al nombre del rol
    # 
    # En lugar de:
    #   rol = db.query(Rol).filter(Rol.id_rol == usuario.id_rol).first()
    #   rol.nombre_rol
    #
    # "Rol" = nombre de la clase (no de la tabla)
    # backref="usuarios" = desde un Rol puedes hacer: rol.usuarios para ver todos sus usuarios
    rol = relationship("Rol", backref="usuarios")
    
    # Nota: Habrán más relationships cuando crees Asignacion, Nota, Auditoria
