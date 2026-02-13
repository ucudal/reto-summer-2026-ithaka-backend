"""
CONFIGURACIÓN
=============
Este archivo maneja todas las variables de entorno de la aplicación.

Las variables se leen desde el archivo .env (que NO se sube a GitHub)

Uso en otros archivos:
    from app.core.config import settings
    
    database_url = settings.DATABASE_URL
    secret_key = settings.SECRET_KEY
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic
    
    Pydantic leerá automáticamente las variables del archivo .env
    y las validará según los tipos que definimos aquí.
    """
    
    # ========== BASE DE DATOS ==========
    # Opción 1: Variables separadas (más flexible)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "ithaka_db"
    
    @property
    def DATABASE_URL(self) -> str:
        """
        Construye la URL de conexión a PostgreSQL
        
        Returns:
            URL de conexión en formato SQLAlchemy
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Opción 2: URL completa (descomenta si prefieres esto)
    # DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ithaka_db"
    
    # ========== SEGURIDAD ==========
    SECRET_KEY: str = "desarrollo-inseguro-cambiar-en-produccion"
    """
    Clave secreta para firmar tokens JWT
    
    IMPORTANTE: Cambiar esto en producción
    Generar con: python -c "import secrets; print(secrets.token_urlsafe(32))"
    """
    
    ALGORITHM: str = "HS256"
    """Algoritmo para JWT"""
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    """Duración del token en minutos"""
    
    # ========== APLICACIÓN ==========
    PROJECT_NAME: str = "Ithaka Backoffice API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # ========== CORS ==========
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    """Orígenes permitidos (separados por comas)"""
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convierte ALLOWED_ORIGINS en lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # ========== CONFIGURACIÓN DE PYDANTIC ==========
    class Config:
        env_file = ".env"  # Lee automáticamente de .env
        case_sensitive = True


# ============================================================================
# INSTANCIA GLOBAL DE CONFIGURACIÓN
# ============================================================================
settings = Settings()
"""
Instancia global de configuración

Ejemplo de uso:
    from app.core.config import settings
    
    print(settings.DATABASE_URL)
    print(settings.SECRET_KEY)
"""