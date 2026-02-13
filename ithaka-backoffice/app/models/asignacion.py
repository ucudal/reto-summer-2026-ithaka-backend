"""
Modelo ASIGNACION
-----------------
Representa la tabla 'asignacion' en PostgreSQL.
Registra qué usuarios (tutores/coordinadores) están asignados a qué casos.
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Asignacion(Base):
    """
    Clase que representa la asignación de un usuario a un caso
    
    Un caso puede tener múltiples asignaciones (varios tutores)
    Un usuario puede estar asignado a múltiples casos
    
    Ejemplo:
        asignacion = Asignacion(
            id_usuario=2,  # ID del tutor
            id_caso=5      # ID del caso
        )
        # fecha_asignacion se pone automáticamente
    """
    
    __tablename__ = "asignacion"
    
    # ID único de la asignación
    id_asignacion = Column(Integer, primary_key=True, index=True)
    
    # Fecha en que se hizo la asignación
    # Se pone automáticamente cuando creas el registro
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    
    # ========== FOREIGN KEYS ==========
    
    # ID del usuario asignado (ej: tutor, coordinador)
    id_usuario = Column(
        Integer, 
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )
    
    # ID del caso al que se asigna
    id_caso = Column(
        Integer, 
        ForeignKey("caso.id_caso"),
        nullable=False
    )
    
    # ========== RELATIONSHIPS ==========
    
    # Acceso al usuario asignado:
    #   asignacion.usuario.nombre ← Nombre del tutor
    #   asignacion.usuario.email
    # backref="asignaciones" permite: usuario.asignaciones ← Todos los casos del usuario
    usuario = relationship("Usuario", backref="asignaciones")
    
    # Acceso al caso:
    #   asignacion.caso.nombre_caso ← Nombre del caso
    #   asignacion.caso.estado.nombre_estado ← Estado del caso
    # backref="asignaciones" permite: caso.asignaciones ← Todos los usuarios asignados
    caso = relationship("Caso", backref="asignaciones")
    
    # Ejemplo de uso en queries:
    # Para ver todos los casos de un tutor:
    #   tutor = db.query(Usuario).filter_by(id_usuario=2).first()
    #   casos_del_tutor = [asig.caso for asig in tutor.asignaciones]
    #
    # Para ver todos los tutores de un caso:
    #   caso = db.query(Caso).filter_by(id_caso=5).first()
    #   tutores = [asig.usuario for asig in caso.asignaciones]
