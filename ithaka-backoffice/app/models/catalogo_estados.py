from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import validates
from app.db.database import Base


class CatalogoEstados(Base):
 
    __tablename__ = "catalogo_estados"
    
    id_estado = Column(Integer, primary_key=True, index=True)
    
    nombre_estado = Column(String(100), nullable=False)

    # Postulacion o Proyecto
    tipo_caso = Column(String(100), nullable=False)

    @validates("nombre_estado")
    def _normalize_nombre_estado(self, key, value):
        return value.lower() if isinstance(value, str) else value

    @validates("tipo_caso")
    def _normalize_tipo_caso(self, key, value):
        return value.lower() if isinstance(value, str) else value
    
    # CheckConstraint: Validación a nivel de base de datos
    # Solo permite los valores 'Postulacion' o 'Proyecto'
    # Esto es equivalente al CHECK
    __table_args__ = (
        CheckConstraint(
            "lower(tipo_caso) IN ('postulacion', 'proyecto')",
            name="check_tipo_caso"
        ),
    )