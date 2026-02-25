from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Asignacion(Base):
    __tablename__ = "asignacion"
    
    # Columnas
    id_asignacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Foreign Keys
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_caso = Column(Integer, ForeignKey("caso.id_caso"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="asignaciones")
    caso = relationship("Caso", back_populates="asignaciones")