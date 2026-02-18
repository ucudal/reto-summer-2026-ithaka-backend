from sqlalchemy import Column, Integer, String, CheckConstraint
from app.db.database import Base


class CatalogoEstados(Base):
 
    __tablename__ = "catalogo_estados"
    
    id_estado = Column(Integer, primary_key=True, index=True)
    
    nombre_estado = Column(String(100), nullable=False)
    
    # Postulacion o Proyecto
    tipo_caso = Column(String(20), nullable=False)
    
    # CheckConstraint: Validación a nivel de base de datos
    # Solo permite los valores 'Postulacion' o 'Proyecto'
    # Esto es equivalente al CHECK
    __table_args__ = (
        CheckConstraint(
            "tipo_caso IN ('Postulacion', 'Proyecto')",
            name="check_tipo_caso"
        ),
    )
    
