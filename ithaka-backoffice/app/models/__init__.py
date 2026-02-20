"""
Módulo de Modelos
-----------------
Este archivo importa todos los modelos para que sean más fáciles de usar.

En lugar de hacer:
    from app.models.usuario import Usuario
    from app.models.caso import Caso

Puedes hacer:
    from app.models import Usuario, Caso

Además, SQLAlchemy necesita que todos los modelos estén importados
para que pueda crear las relaciones correctamente.
"""

# Modelos base (sin dependencias)
from app.models.emprendedor import Emprendedor
from app.models.catalogo_estados import CatalogoEstados
from app.models.convocatoria import Convocatoria
from app.models.programa import Programa
from app.models.apoyo import Apoyo

# Modelos con foreign keys
from app.models.caso import Caso
from app.models.nota import Nota
from app.models.auditoria import Auditoria


# Esto permite hacer: from app.models import Usuario, Caso, etc.
__all__ = [
    "Emprendedor",
    "CatalogoEstados",
    "Caso",
    "Nota",
    "Auditoria",
    "Convocatoria",
    "Programa",
    "Apoyo",
]
