from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from app.models import Emprendedor

# Configuración del correo
conf = ConnectionConfig(
    MAIL_USERNAME="tu_email@example.com",
    MAIL_PASSWORD="tu_contraseña",
    MAIL_FROM="tu_email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.example.com",
    MAIL_FROM_NAME="Nombre del Remitente",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

# Función para enviar correos
async def send_email(email: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],  # Lista de correos
        body=body,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

# Función para manejar cambios en el caso
async def notificar_cambio_estado(caso_id: int, nombre_estado: str, db: Session):
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    if not caso:
        return

    emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == caso.id_emprendedor).first()
    if emprendedor:
        await send_email(
            email=emprendedor.email,
            subject="Cambio de Estado de Caso",
            body=f"El estado del caso {caso_id} ha cambiado a {nombre_estado}."
        )

# Función para manejar cambios en la asignación
async def notificar_cambio_asignacion(asignacion_id: int, db: Session):
    asignacion = db.query(Asignacion).filter(Asignacion.id_asignacion == asignacion_id).first()
    if not asignacion:
        return

    emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == asignacion.id_emprendedor).first()
    if emprendedor:
        await send_email(
            email=emprendedor.email,
            subject="Cambio de Asignación de Caso",
            body=f"El tutor asignado al caso {asignacion.id_caso} ha cambiado."
        )