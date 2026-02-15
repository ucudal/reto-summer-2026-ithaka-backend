"""
DEPENDENCIES (DEPS)
===================
Este archivo contiene "dependencies" que se reutilizan en múltiples endpoints.

En lugar de duplicar código, IMPORTAMOS get_db desde db.session
"""

# ============================================================================
# IMPORTAR DEPENDENCIES DESDE OTROS MÓDULOS
# ============================================================================

# get_db() está definido en db/session.py
# Lo importamos aquí para tenerlo disponible junto a otras dependencies
from app.db.session import get_db

# Exportamos get_db para que otros archivos puedan importarlo desde aquí
# Uso: from app.api.deps import get_db
__all__ = ["get_db"]

