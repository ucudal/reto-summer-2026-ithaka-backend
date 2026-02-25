from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Caso(Base):
    __tablename__ = "caso"
    
    # Columnas básicas
    id_caso = Column(Integer, primary_key=True, index=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    nombre_caso = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Datos del chatbot (JSON)
    datos_chatbot = Column(JSON)
    
    # Foreign Keys
    id_emprendedor = Column(Integer, ForeignKey("emprendedor.id_emprendedor"), nullable=False)
    id_convocatoria = Column(Integer, ForeignKey("convocatoria.id_convocatoria"))
    id_estado = Column(Integer, ForeignKey("catalogo_estados.id_estado"), nullable=False)
    
    # Relationships
    emprendedor = relationship("Emprendedor", backref="casos")
    convocatoria = relationship("Convocatoria", backref="casos")
    estado = relationship("CatalogoEstados", backref="casos")
    asignaciones = relationship("Asignacion", back_populates="caso")