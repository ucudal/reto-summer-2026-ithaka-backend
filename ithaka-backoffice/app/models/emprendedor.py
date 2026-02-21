
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base


class Emprendedor(Base):

    __tablename__ = "emprendedor"
    
    id_emprendedor = Column(Integer, primary_key=True, index=True)
    
    nombre = Column(String(150), nullable=False)
    apellido = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    telefono = Column(String(50), nullable=True)
    documento_identidad = Column(String(50), nullable=True)
    pais_residencia = Column(String(100), nullable=True)
    ciudad_residencia = Column(String(100), nullable=True)
    campus_ucu = Column(String(100), nullable=True)
    relacion_ucu = Column(String(100), nullable=True)
    facultad_ucu = Column(String(100), nullable=True)
    canal_llegada = Column(String(100), nullable=True)
    motivacion = Column(String, nullable=True)  # TEXT
    fecha_registro = Column(DateTime, default=datetime.utcnow)

