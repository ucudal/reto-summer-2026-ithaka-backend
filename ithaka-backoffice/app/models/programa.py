from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class Programa(Base):
    __tablename__ = "programa"

    id_programa = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    apoyos = relationship("Apoyo", backref="programa", lazy="selectin")