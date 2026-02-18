from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Caso(Base):
    
    
    __tablename__ = "caso"
    
    # ========== COLUMNAS BÁSICAS ==========
    
    id_caso = Column(Integer, primary_key=True, index=True)
    
   
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    nombre_caso = Column(String(200), nullable=False)
    
    
    descripcion = Column(Text)
    
    # ========== DATOS DEL CHATBOT ==========
    # JSONB = tipo especial de PostgreSQL para guardar JSON
    # Puede guardar cualquier estructura JSON:
    # {"edad": 25, "sector": "Tecnología", "respuestas": ["a", "b", "c"]}
    # Ejemplo: SELECT * FROM caso WHERE datos_chatbot->>'sector' = 'Tecnología'
    datos_chatbot = Column(JSONB)
    
    consentimiento_datos = Column(Boolean, default=False)
    
    # ========== FOREIGN KEYS ==========
    
    id_emprendedor = Column(
        Integer, 
        ForeignKey("emprendedor.id_emprendedor"),
        nullable=False
    )
    
    id_convocatoria = Column(
        Integer, 
        ForeignKey("convocatoria.id_convocatoria")
    )
    
    id_estado = Column(
        Integer, 
        ForeignKey("catalogo_estados.id_estado"),
        nullable=False
    )
    
    # ========== RELATIONSHIPS ==========
    # Estas NO son columnas, son helpers para acceder a objetos relacionados
    
    # Acceso al emprendedor:
    #   caso.emprendedor.nombre ← Obtiene el nombre del emprendedor
    #   caso.emprendedor.email  ← Obtiene el email
    # backref="casos" permite hacer: emprendedor.casos ← Todos los casos del emprendedor
    emprendedor = relationship("Emprendedor", backref="casos")
    
    # Acceso a la convocatoria:
    # COMENTADO: El modelo Convocatoria no existe todavía
    # convocatoria = relationship("Convocatoria", backref="casos")
    
    # Acceso al estado:
    #   caso.estado.nombre_estado ← "En Revisión"
    #   caso.estado.tipo_caso ← "Postulacion"
    estado = relationship("CatalogoEstados", backref="casos")
    
    # Nota: Más relationships se agregarán cuando tengas Apoyo, Asignacion, Nota, Auditoria
    # Por ejemplo:
    #   caso.apoyos ← Lista de apoyos/programas asignados a este caso
    #   caso.asignaciones ← Usuarios (tutores) asignados a este caso
    #   caso.notas ← Notas/comentarios sobre este caso
