"""
Modelo NOTA
-----------
Representa la tabla 'nota' en PostgreSQL.
Almacena comentarios/notas que los usuarios hacen sobre los casos.
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Nota(Base):
    """
    Clase que representa una nota/comentario sobre un caso
    
    Los usuarios pueden dejar notas sobre los casos que gestionan
    
    Ejemplo:
        nota = Nota(
            contenido="El emprendedor presentó documentación adicional",
            id_usuario=2,  # Quién escribió la nota
            id_caso=5      # Sobre qué caso
        )
    """
    
    __tablename__ = "nota"
    
    # ID único de la nota
    id_nota = Column(Integer, primary_key=True, index=True)
    
    # Contenido de la nota (puede ser texto largo)
    # Text = sin límite de caracteres
    contenido = Column(Text, nullable=False)
    
    # Fecha y hora en que se creó la nota
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # ========== FOREIGN KEYS ==========
    
    # ID del usuario que escribió la nota
    id_usuario = Column(
        Integer, 
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )
    
    # ID del caso sobre el que se escribe la nota
    id_caso = Column(
        Integer, 
        ForeignKey("caso.id_caso"),
        nullable=False
    )
    
    # ========== RELATIONSHIPS ==========
    
    # Acceso al usuario que escribió:
    #   nota.usuario.nombre ← "Ana García"
    #   nota.usuario.email
    # backref="notas" permite: usuario.notas ← Todas las notas del usuario
    usuario = relationship("Usuario", backref="notas")
    
    # Acceso al caso:
    #   nota.caso.nombre_caso ← Nombre del caso
    #   nota.caso.emprendedor.nombre ← Nombre del emprendedor
    # backref="notas" permite: caso.notas ← Todas las notas del caso
    caso = relationship("Caso", backref="notas")
    
    # Ejemplo de uso:
    # Ver todas las notas de un caso ordenadas por fecha:
    #   notas = db.query(Nota).filter_by(id_caso=5).order_by(Nota.fecha.desc()).all()
    #   for nota in notas:
    #       print(f"{nota.fecha} - {nota.usuario.nombre}: {nota.contenido}")
