"""
Modelo EMPRENDEDOR
------------------
Representa la tabla 'emprendedor' en PostgreSQL.
Almacena información de las personas que presentan ideas/proyectos.
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base


class Emprendedor(Base):
    """
    Clase que representa a un emprendedor
    
    Ejemplo de uso:
        emprendedor = Emprendedor(
            nombre="Juan Pérez",
            email="juan@example.com",
            telefono="+598 99 123 456",
            vinculo_institucional="Estudiante UCU"
        )
    """
    
    __tablename__ = "emprendedor"
    
    # ID único del emprendedor
    id_emprendedor = Column(Integer, primary_key=True, index=True)
    
    # Nombre completo del emprendedor
    # String(150) = hasta 150 caracteres
    # nullable=False = obligatorio
    nombre = Column(String(150), nullable=False)
    
    # Email del emprendedor
    email = Column(String(150), nullable=False)
    
    # Teléfono (opcional, por eso no tiene nullable=False)
    # Si no ponés nullable=False, por defecto es nullable=True
    telefono = Column(String(50))
    
    # Relación con la universidad (ej: "Estudiante", "Egresado", "Externo")
    vinculo_institucional = Column(String(150))
    
    # Fecha en que se registró en el sistema
    # DateTime = tipo fecha y hora
    # default=datetime.utcnow = si no le pasas valor, pone la fecha/hora actual
    # Nota: utcnow (sin paréntesis) pasa la FUNCIÓN, no la ejecuta inmediatamente
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Nota sobre las relaciones:
    # Este modelo TENDRÁ una relación con "Caso" (un emprendedor puede tener muchos casos)
    # Esa relación se define en el modelo Caso, no acá
