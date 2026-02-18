
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base


class Emprendedor(Base):

    __tablename__ = "emprendedor"
    
    id_emprendedor = Column(Integer, primary_key=True, index=True)
    

    nombre = Column(String(150), nullable=False)
    
    email = Column(String(150), nullable=False)
    
    telefono = Column(String(50))
    
    vinculo_institucional = Column(String(150))
    
    # Fecha en que se registró en el sistema
    # DateTime = tipo fecha y hora
    # default=datetime.utcnow = si no se le pasa valor, pone la fecha/hora actual
    fecha_registro = Column(DateTime, default=datetime.utcnow)

