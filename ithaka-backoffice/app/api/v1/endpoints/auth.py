"""
Endpoints de autenticación: login, logout, obtener usuario actual
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.schemas.auth import LoginRequest, LoginResponse, UsuarioActual

from app.api.deps import get_db
from app.models.usuario import Usuario
from app.core.security import (
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login de usuario
    
    **Proceso:**
    1. Envías email y password
    2. El servidor verifica las credenciales
    3. Si son correctas, recibes un JWT token
    4. Usas ese token en todos los requests protegidos
    
    **Cómo usar el token:**
    - En Swagger: Click "Authorize" arriba a la derecha, pega `Bearer {tu_token}`
    - En código: Header `Authorization: Bearer {tu_token}`
    - El token expira en 30 minutos por defecto
    
    **Ejemplo:**
    ```
    POST /api/v1/auth/login
    {
      "email": "admin@ithaka.com",
      "password": "admin123"
    }
    
    Respuesta:
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "usuario": {
        "id": 1,
        "nombre": "Admin",
        "email": "admin@ithaka.com",
        "rol": "admin"
      }
    }
    ```
    """
    # 1. Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Verificar password
    if not verify_password(credentials.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Verificar que el usuario esté activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado. Contacta al administrador."
        )
    
    # 4. Crear token JWT con información del usuario
    access_token = create_access_token(
        data={
            "sub": str(usuario.id_usuario),  # "sub" = subject (estándar JWT)
            "email": usuario.email,
            "rol": usuario.rol.nombre_rol if usuario.rol else None
        }
    )
    
    # 5. Devolver token y información del usuario
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id_usuario,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol.nombre_rol if usuario.rol else None
        }
    }


@router.get("/me", response_model=UsuarioActual)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """
    Obtener información del usuario actual (autenticado)
    
    **Requiere autenticación:** Sí - Debes enviar el JWT token en el header
    
    **Cómo funciona:**
    1. Lee el token del header `Authorization: Bearer {token}`
    2. Decodifica el token y extrae el ID del usuario
    3. Busca el usuario en la base de datos
    4. Devuelve la información del usuario
    
    **Útil para:**
    - Verificar que tu token funciona correctamente
    - Obtener info del usuario logueado en el frontend
    - Verificar permisos antes de mostrar opciones en el UI
    
    **Ejemplo:**
    ```
    GET /api/v1/auth/me
    Headers: {
      "Authorization": "Bearer eyJhbGci..."
    }
    
    Respuesta:
    {
      "id_usuario": 1,
      "nombre": "Administrador",
      "email": "admin@ithaka.com",
      "rol": "admin"
    }
    ```
    """
    return {
        "id_usuario": current_user.id_usuario,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "rol": current_user.rol.nombre_rol if current_user.rol else None
    }


@router.post("/logout")
def logout(current_user: Usuario = Depends(get_current_user)):
    """
    Logout de usuario
    
    **Nota:** Con JWT, el logout es manejado principalmente por el cliente.
    El cliente debe eliminar el token de localStorage/cookies.
    
    Este endpoint existe principalmente para:
    - Registrar en logs cuando un usuario hace logout
    - Invalidar tokens (si implementas una blacklist)
    - Limpiar sesiones adicionales si las hubiera
    
    **En el frontend:**
    ```javascript
    // Hacer logout
    await api.post('/auth/logout');
    localStorage.removeItem('access_token');
    ```
    """
    # Aquí podrías agregar lógica adicional como:
    # - Registrar en logs
    # - Agregar token a blacklist
    # - Limpiar otras sesiones
    
    return {
        "message": "Logout exitoso",
        "detail": "Elimina el token del cliente (localStorage/cookies)"
    }