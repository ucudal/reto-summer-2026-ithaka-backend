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
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic
    
    Pydantic leerá automáticamente las variables del archivo .env
    y las validará según los tipos que definimos aquí.
    """
    
    # ========== BASE DE DATOS ==========
    # Variables separadas (más flexible)
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
    
    # ========== SEGURIDAD ==========
    SECRET_KEY: str = "desarrollo-inseguro-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ========== APP ==========
    PROJECT_NAME: str = "Ithaka Backoffice"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # ========== CORS ==========
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'  # Ignora campos extra del .env que no estén definidos
    )


# Instancia global de settings
settings = Settings()
