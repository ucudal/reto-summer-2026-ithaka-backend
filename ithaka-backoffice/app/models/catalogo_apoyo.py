from sqlalchemy import Column, Integer, String, Text, Boolean
from app.db.database import Base

class CatalogoApoyo(Base):
    __tablename__ = "catalogo_apoyo"

    id_catalogo_apoyo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), unique=True, nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
