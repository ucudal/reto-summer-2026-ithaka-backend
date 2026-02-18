from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class Convocatoria(Base):
    __tablename__ = "convocatoria"

    id_convocatoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    fecha_cierre = Column(DateTime, nullable=True)

    casos = relationship("Caso", backref="convocatoria", lazy="selectin")