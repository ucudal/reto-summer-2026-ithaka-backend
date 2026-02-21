from pydantic import BaseModel, EmailStr
class LoginRequest(BaseModel):
    """Schema para el request de login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@ithaka.com",
                "password": "admin123"
            }
        }


class LoginResponse(BaseModel):
    """Schema para la respuesta del login"""
    access_token: str
    token_type: str = "bearer"
    usuario: dict


class UsuarioActual(BaseModel):
    """Schema para información del usuario actual"""
    id_usuario: int
    nombre: str
    email: str
    rol: str


