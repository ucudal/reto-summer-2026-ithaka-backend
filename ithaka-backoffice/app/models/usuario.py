"""
Modelo USUARIO
--------------
TODO: Implementar usando TEMPLATE.py como guía

Tabla: usuario
Columnas según SQL:
- id_usuario SERIAL PRIMARY KEY
- nombre VARCHAR(150) NOT NULL
- email VARCHAR(150) NOT NULL UNIQUE
- password_hash TEXT NOT NULL
- activo BOOLEAN DEFAULT TRUE
- id_rol INTEGER NOT NULL (FK a rol)
"""

# from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.database import Base
# 
# class Usuario(Base):
#     __tablename__ = "usuario"
#     # ... agregar columnas

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import Usuario, Rol

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

"""Get /usuarios"""
@router.get("/")
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.activo == True).all()

"""GET /usuarios/{id}"""
@router.get("/{id}")
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

"""POST /usuarios"""
@router.post("/")
def crear_usuario(
    nombre: str,
    email: str,
    password: str,
    id_rol: int,
    db: Session = Depends(get_db)
):
    rol = db.query(Rol).filter(Rol.id == id_rol).first()
    if not rol:
        raise HTTPException(status_code=400, detail="Rol inválido")

    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        password_hash=hash_password(password),
        id_rol=id_rol,
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"mensaje": "Usuario creado correctamente"}

"""PUT /usuarios/{id}"""
@router.put("/{id}")
def actualizar_usuario( 
    id: int,
    nombre: str = None,
    email: str = None,
    password: str = None,
    id_rol: int = None,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if nombre:
        usuario.nombre = nombre
    if email:
        usuario.email = email
    if password:
        usuario.password_hash = hash_password(password)
    if id_rol:
        rol = db.query(Rol).filter(Rol.id == id_rol).first()
        if not rol:
            raise HTTPException(status_code=400, detail="Rol inválido")
        usuario.id_rol = id_rol

    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Usuario actualizado correctamente", "usuario": usuario}     

"""DELETE /usuarios/{id}"""
@router.delete("/{id}")
def desactivar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = False
    db.commit()

    return {"mensaje": "Usuario desactivado correctamente"}
