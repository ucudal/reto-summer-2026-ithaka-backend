"""
Módulo de seguridad: JWT, passwords y autenticación
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.deps import get_db
from app.models.usuario import Usuario


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Esquema de seguridad HTTP Bearer (para Swagger UI)
security = HTTPBearer()


# ============================================================================
# FUNCIONES PARA PASSWORDS
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hashear un password antes de guardarlo en la base de datos
    
    Args:
        password: Password en texto plano
    
    Returns:
        Hash del password (string largo)
    
    Ejemplo:
        >>> hash_password("admin123")
        "$2b$12$KIXv5McSxK9Y7J3..."
    """
    # Convertir password a bytes y hashear con bcrypt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar si un password coincide con su hash
    
    Args:
        plain_password: Password ingresado por el usuario
        hashed_password: Hash guardado en la BD
    
    Returns:
        True si coinciden, False si no
    
    Ejemplo:
        >>> verify_password("admin123", "$2b$12$KIXv5McSxK9Y7J3...")
        True
        >>> verify_password("wrongpass", "$2b$12$KIXv5McSxK9Y7J3...")
        False
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        # Si hay algún error al verificar (hash corrupto, etc.)
        print(f"Error verificando password: {e}")
        return False



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crear un JWT token
    
    Args:
        data: Diccionario con información a incluir en el token
              Ejemplo: {"sub": "5", "email": "user@example.com"}
        expires_delta: Cuánto tiempo será válido el token
    
    Returns:
        JWT token como string
    
    Ejemplo:
        >>> token = create_access_token({"sub": "5", "email": "admin@ithaka.com"})
        >>> print(token)
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1Ii..."
    """
    to_encode = data.copy()
    
    # Calcular fecha de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Agregar expiración al payload
    to_encode.update({"exp": expire})
    
    # Crear el token firmado con SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodificar un JWT token y extraer su información
    
    Args:
        token: El JWT token a decodificar
    
    Returns:
        Diccionario con la información del token
    
    Raises:
        HTTPException: Si el token es inválido o expiró
    
    Ejemplo:
        >>> payload = decode_access_token("eyJhbGci...")
        >>> print(payload)
        {"sub": "5", "email": "admin@ithaka.com", "exp": 1708228800}
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================================
# DEPENDENCIES PARA ENDPOINTS
# ============================================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependency que extrae el usuario autenticado del JWT token
    
    Se usa en endpoints protegidos para obtener el usuario actual:
    
    Ejemplo de uso:
        @router.get("/casos")
        def listar_casos(
            current_user: Usuario = Depends(get_current_user),
            db: Session = Depends(get_db)
        ):
            print(f"Usuario: {current_user.nombre}")
            # ...
    
    Args:
        credentials: Token extraído del header Authorization
        db: Sesión de base de datos
    
    Returns:
        Usuario autenticado
    
    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    # Extraer el token del header Authorization: Bearer <token>
    token = credentials.credentials
    
    # Decodificar el token
    payload = decode_access_token(token)
    
    # Extraer el ID del usuario del token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta ID de usuario",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Buscar el usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return usuario


def require_role(allowed_roles: list[str]):
    """
    Dependency factory para verificar que el usuario tenga un rol específico
    
    Ejemplo de uso:
        @router.delete("/casos/{id}")
        def eliminar_caso(
            id: int,
            current_user: Usuario = Depends(require_role(["admin", "superadmin"]))
        ):
            # Solo admin o superadmin pueden ejecutar esto
            ...
    
    Args:
        allowed_roles: Lista de roles permitidos (ej: ["admin", "superadmin"])
    
    Returns:
        Función de dependency que verifica el rol
    """
    def role_checker(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        # Obtener el nombre del rol del usuario
        rol_nombre = current_user.rol.nombre_rol if current_user.rol else None
        
        # Verificar si el rol está en la lista de roles permitidos
        if rol_nombre not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere rol: {', '.join(allowed_roles)}. Tu rol: {rol_nombre}"
            )
        
        return current_user
    
    return role_checker


def get_current_active_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """
    Dependency que verifica que el usuario sea administrador
    
    Atajo para require_role(["admin"])
    
    Ejemplo de uso:
        @router.delete("/usuarios/{id}")
        def eliminar_usuario(
            id: int,
            current_user: Usuario = Depends(get_current_active_admin)
        ):
            # Solo admin puede ejecutar esto
            ...
    """
    if not current_user.rol or current_user.rol.nombre_rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador"
        )
    return current_user