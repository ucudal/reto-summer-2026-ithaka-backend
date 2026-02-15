"""
Modelo CATALOGO_ESTADOS
------------------------
Representa la tabla 'catalogo_estados' en PostgreSQL.
Define los posibles estados para postulaciones y proyectos.
"""

from sqlalchemy import Column, Integer, String, CheckConstraint
from app.db.database import Base


class CatalogoEstados(Base):
    """
    Clase que representa un estado del catálogo
    
    Puede ser para:
    - Postulaciones: "recibida", "en_revision", "aprobada", "rechazada"
    - Proyectos: "activo", "pausado", "finalizado"
    
    Ejemplo:
        estado = CatalogoEstados(
            nombre_estado="En Revisión",
            tipo_caso="Postulacion"
        )
    """
    
    __tablename__ = "catalogo_estados"
    
    # ID único del estado
    id_estado = Column(Integer, primary_key=True, index=True)
    
    # Nombre del estado (ej: "En Revisión", "Aprobada", "Rechazada")
    nombre_estado = Column(String(100), nullable=False)
    
    # Tipo de caso al que aplica: "Postulacion" o "Proyecto"
    # String(20) porque solo guardamos estas dos palabras
    tipo_caso = Column(String(20), nullable=False)
    
    # CheckConstraint: Validación a nivel de base de datos
    # Solo permite los valores 'Postulacion' o 'Proyecto'
    # Esto es equivalente al CHECK que tenías en SQL
    __table_args__ = (
        CheckConstraint(
            "tipo_caso IN ('Postulacion', 'Proyecto')",
            name="check_tipo_caso"
        ),
    )
    
    # Nota: En Python usarías Enum para validar, pero en la DB
    # este CheckConstraint asegura que nadie meta valores incorrectos
