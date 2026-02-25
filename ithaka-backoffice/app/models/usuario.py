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
    asignaciones = relationship("Asignacion", back_populates="usuario")
    # notas = relationship("Nota", back_populates="usuario")  # puedes descomentar si existe modelo Nota
    
    def __repr__(self):
        """Representación que NO incluye password_hash por seguridad"""
        return (
            f"<Usuario(id={self.id_usuario}, nombre='{self.nombre}', "
            f"email='{self.email}', rol_id={self.id_rol}, activo={self.activo})>"
        )