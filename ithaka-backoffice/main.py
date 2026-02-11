from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="Ithaka Backoffice API",
    description="API para gestión de postulaciones del Centro de Emprendimiento e Innovación - UCU",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class PostulacionEstado(str, Enum):
    BORRADOR = "borrador"
    RECIBIDA = "recibida"
    EN_REVISION = "en_revision"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"

# Modelos
class PostulacionCreate(BaseModel):
    nombre_emprendedor: str
    email: EmailStr
    telefono: str
    nombre_idea: str
    descripcion: str
    vinculo_institucional: Optional[str] = None

class Postulacion(BaseModel):
    id: int
    nombre_emprendedor: str
    email: EmailStr
    telefono: str
    nombre_idea: str
    descripcion: str
    vinculo_institucional: Optional[str] = None
    estado: PostulacionEstado
    fecha_creacion: datetime
    tutor_asignado: Optional[str] = None

# Base de datos en memoria (temporal)
postulaciones_db: List[Postulacion] = []
counter = 1

# Endpoints
@app.get("/")
async def root():
    """Endpoint raíz - health check"""
    return {
        "message": "Ithaka Backoffice API",
        "status": "operational",
        "version": "0.1.0"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/postulaciones", response_model=Postulacion, status_code=201)
async def crear_postulacion(postulacion: PostulacionCreate):
    """Crear una nueva postulación desde el chatbot"""
    global counter
    
    nueva_postulacion = Postulacion(
        id=counter,
        nombre_emprendedor=postulacion.nombre_emprendedor,
        email=postulacion.email,
        telefono=postulacion.telefono,
        nombre_idea=postulacion.nombre_idea,
        descripcion=postulacion.descripcion,
        vinculo_institucional=postulacion.vinculo_institucional,
        estado=PostulacionEstado.RECIBIDA,
        fecha_creacion=datetime.now()
    )
    
    postulaciones_db.append(nueva_postulacion)
    counter += 1
    
    return nueva_postulacion

@app.get("/api/postulaciones", response_model=List[Postulacion])
async def listar_postulaciones(estado: Optional[PostulacionEstado] = None):
    """Listar todas las postulaciones con filtro opcional por estado"""
    if estado:
        return [p for p in postulaciones_db if p.estado == estado]
    return postulaciones_db

@app.get("/api/postulaciones/{postulacion_id}", response_model=Postulacion)
async def obtener_postulacion(postulacion_id: int):
    """Obtener detalle de una postulación específica"""
    for postulacion in postulaciones_db:
        if postulacion.id == postulacion_id:
            return postulacion
    
    raise HTTPException(status_code=404, detail="Postulación no encontrada")

@app.get("/api/stats")
async def obtener_estadisticas():
    """Obtener estadísticas básicas de postulaciones"""
    total = len(postulaciones_db)
    
    stats_por_estado = {}
    for estado in PostulacionEstado:
        count = len([p for p in postulaciones_db if p.estado == estado])
        stats_por_estado[estado.value] = count
    
    return {
        "total_postulaciones": total,
        "por_estado": stats_por_estado
    }
