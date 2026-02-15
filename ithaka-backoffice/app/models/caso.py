"""
Modelo CASO
-----------
Representa la tabla 'caso' en PostgreSQL.
Es la tabla CENTRAL del sistema. Representa tanto postulaciones como proyectos.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Caso(Base):
    """
    Clase que representa un caso (postulación o proyecto)
    
    Ciclo de vida:
    1. Se crea como postulación (estado: "recibida")
    2. Pasa a revisión (estado: "en_revision")
    3. Se aprueba (estado: "aprobada") → puede convertirse en proyecto
    4. O se rechaza (estado: "rechazada")
    
    Ejemplo de uso:
        caso = Caso(
            nombre_caso="EcoApp - Gestión de residuos",
            descripcion="Una app para...",
            datos_chatbot={"edad": 25, "sector": "tecnología"},
            consentimiento_datos=True,
            id_emprendedor=1,
            id_convocatoria=2,
            id_estado=1  # ID del estado "recibida"
        )
    """
    
    __tablename__ = "caso"
    
    # ========== COLUMNAS BÁSICAS ==========
    
    # ID único del caso
    id_caso = Column(Integer, primary_key=True, index=True)
    
    # Fecha en que se creó el caso
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Nombre del caso/proyecto (ej: "EcoApp - Reciclaje inteligente")
    nombre_caso = Column(String(200), nullable=False)
    
    # Descripción detallada del caso
    # Text = sin límite de caracteres (para textos largos)
    descripcion = Column(Text)
    
    # ========== DATOS DEL CHATBOT ==========
    # JSONB = tipo especial de PostgreSQL para guardar JSON
    # Puede guardar cualquier estructura JSON:
    # {"edad": 25, "sector": "Tecnología", "respuestas": ["a", "b", "c"]}
    #
    # Ventaja: Puedes hacer queries JSON dentro de PostgreSQL
    # Ejemplo: SELECT * FROM caso WHERE datos_chatbot->>'sector' = 'Tecnología'
    datos_chatbot = Column(JSONB)
    
    # Si el emprendedor aceptó que usemos sus datos
    consentimiento_datos = Column(Boolean, default=False)
    
    # ========== FOREIGN KEYS ==========
    
    # ID del emprendedor que presentó este caso
    # nullable=False = SIEMPRE debe tener un emprendedor
    id_emprendedor = Column(
        Integer, 
        ForeignKey("emprendedor.id_emprendedor"),
        nullable=False
    )
    
    # ID de la convocatoria (puede ser NULL si no aplica a ninguna)
    # Ejemplo: casos creados fuera de convocatoria
    id_convocatoria = Column(
        Integer, 
        ForeignKey("convocatoria.id_convocatoria")
    )
    
    # ID del estado actual (ej: "recibida", "en_revision", etc.)
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
    #   caso.convocatoria.nombre ← Nombre de la convocatoria
    #   caso.convocatoria.fecha_cierre
    convocatoria = relationship("Convocatoria", backref="casos")
    
    # Acceso al estado:
    #   caso.estado.nombre_estado ← "En Revisión"
    #   caso.estado.tipo_caso ← "Postulacion"
    estado = relationship("CatalogoEstados", backref="casos")
    
    # Nota: Más relationships se agregarán cuando tengas Apoyo, Asignacion, Nota, Auditoria
    # Por ejemplo:
    #   caso.apoyos ← Lista de apoyos/programas asignados a este caso
    #   caso.asignaciones ← Usuarios (tutores) asignados a este caso
    #   caso.notas ← Notas/comentarios sobre este caso
