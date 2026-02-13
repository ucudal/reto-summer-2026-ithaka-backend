"""
Modelo APOYO
------------
Representa la tabla 'apoyo' en PostgreSQL.
Relaciona casos con programas (ej: un caso recibe apoyo del "Programa de Incubación").
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Apoyo(Base):
    """
    Clase que representa un apoyo otorgado a un caso
    
    Un caso puede tener varios apoyos de diferentes programas
    
    Ejemplo:
        apoyo = Apoyo(
            tipo_apoyo="Mentoría técnica",
            fecha_inicio=date(2026, 2, 1),
            fecha_fin=date(2026, 5, 1),
            id_caso=5,
            id_programa=1
        )
    """
    
    __tablename__ = "apoyo"
    
    # ID único del apoyo
    id_apoyo = Column(Integer, primary_key=True, index=True)
    
    # Tipo de apoyo (ej: "Mentoría", "Financiamiento", "Espacios")
    tipo_apoyo = Column(String(150), nullable=False)
    
    # Fecha de inicio del apoyo
    # Date = solo fecha, sin hora (diferente a DateTime)
    fecha_inicio = Column(Date)
    
    # Fecha de fin del apoyo
    fecha_fin = Column(Date)
    
    # ========== FOREIGN KEYS ==========
    
    # ID del caso que recibe el apoyo
    # nullable=False = siempre debe estar asociado a un caso
    id_caso = Column(
        Integer, 
        ForeignKey("caso.id_caso"),
        nullable=False
    )
    
    # ID del programa que brinda el apoyo
    id_programa = Column(
        Integer, 
        ForeignKey("programa.id_programa"),
        nullable=False
    )
    
    # ========== RELATIONSHIPS ==========
    
    # Acceso al caso:
    #   apoyo.caso.nombre_caso ← Nombre del caso que recibe este apoyo
    # backref="apoyos" permite: caso.apoyos ← Lista de todos los apoyos del caso
    caso = relationship("Caso", backref="apoyos")
    
    # Acceso al programa:
    #   apoyo.programa.nombre ← Nombre del programa
    #   apoyo.programa.activo ← Si el programa está activo
    # backref="apoyos" permite: programa.apoyos ← Todos los apoyos de este programa
    programa = relationship("Programa", backref="apoyos")
