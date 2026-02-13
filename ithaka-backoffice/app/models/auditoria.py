"""
Modelo AUDITORIA
----------------
Representa la tabla 'auditoria' en PostgreSQL.
Registra TODOS los cambios importantes que se hacen en los casos (quién, cuándo, qué cambió).
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Auditoria(Base):
    """
    Clase que representa un registro de auditoría
    
    Cada vez que se modifica algo importante en un caso, se crea un registro aquí
    Es como un "historial de cambios" que no se puede borrar
    
    Ejemplo:
        # Cuando un tutor cambia el estado de un caso:
        auditoria = Auditoria(
            accion="Cambio de estado",
            valor_anterior="En revisión",
            valor_nuevo="Aprobada",
            id_usuario=2,  # Quién hizo el cambio
            id_caso=5      # En qué caso
        )
        # timestamp se pone automáticamente
    """
    
    __tablename__ = "auditoria"
    
    # ID único del registro de auditoría
    id_auditoria = Column(Integer, primary_key=True, index=True)
    
    # Timestamp del cambio (fecha y hora exactas)
    # Se guarda automáticamente cuando se crea el registro
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Descripción de la acción realizada
    # Ejemplos:
    #   - "Cambio de estado"
    #   - "Asignación de tutor"
    #   - "Modificación de descripción"
    #   - "Actualización de datos"
    accion = Column(String(150), nullable=False)
    
    # Valor ANTES del cambio
    # Text porque puede ser un valor largo
    # Ejemplo: "En revisión" (antes era este estado)
    valor_anterior = Column(Text)
    
    # Valor DESPUÉS del cambio
    # Ejemplo: "Aprobada" (ahora es este estado)
    valor_nuevo = Column(Text)
    
    # ========== FOREIGN KEYS ==========
    
    # ID del usuario que realizó el cambio
    # Así sabemos QUIÉN hizo cada modificación
    id_usuario = Column(
        Integer, 
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )
    
    # ID del caso que fue modificado
    id_caso = Column(
        Integer, 
        ForeignKey("caso.id_caso"),
        nullable=False
    )
    
    # ========== RELATIONSHIPS ==========
    
    # Acceso al usuario que hizo el cambio:
    #   auditoria.usuario.nombre ← "Ana García"
    #   auditoria.usuario.email
    # backref="auditorias" permite: usuario.auditorias ← Todos los cambios del usuario
    usuario = relationship("Usuario", backref="auditorias")
    
    # Acceso al caso modificado:
    #   auditoria.caso.nombre_caso
    # backref="auditorias" permite: caso.auditorias ← Historial completo del caso
    caso = relationship("Caso", backref="auditorias")
    
    # Ejemplo de uso:
    # Ver el historial completo de cambios de un caso:
    #   historial = db.query(Auditoria).filter_by(id_caso=5).order_by(Auditoria.timestamp.desc()).all()
    #   for registro in historial:
    #       print(f"{registro.timestamp} - {registro.usuario.nombre}")
    #       print(f"  Acción: {registro.accion}")
    #       print(f"  De: {registro.valor_anterior} → A: {registro.valor_nuevo}")
    #
    # Ver todas las acciones de un usuario:
    #   acciones = db.query(Auditoria).filter_by(id_usuario=2).all()
