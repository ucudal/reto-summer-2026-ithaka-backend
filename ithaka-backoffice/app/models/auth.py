from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from database import get_db
from models import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

SECRET_KEY = "clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_password(password_plana, password_hash):
    return pwd_context.verify(password_plana, password_hash)

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(
        Usuario.email == email,
        Usuario.activo == True
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not verificar_password(password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token({
        "id_usuario": usuario.id,
        "rol": usuario.rol.nombre
    })

    return {
        "token": token,
        "usuario": {
            "id_usuario": usuario.id,
            "nombre": usuario.nombre,
            "rol": usuario.rol.nombre
        }
    }
