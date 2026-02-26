import os
import smtplib
import time
import re
import logging
from email.message import EmailMessage

from app.db.database import SessionLocal
from app.models.caso import Caso
from app.models.asignacion import Asignacion
from app.models.emprendedor import Emprendedor
from app.models.usuario import Usuario

MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
MAIL_PORT = int(os.getenv("MAIL_PORT", "1025"))
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() in ("1", "true", "yes")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in ("1", "true", "yes")
MAIL_TIMEOUT = int(os.getenv("MAIL_TIMEOUT", "10"))
MAIL_RETRIES = int(os.getenv("MAIL_RETRIES", "1"))

logger = logging.getLogger(__name__)


def send_email(email: str, subject: str, body: str) -> bool:
    """Send an email using configured SMTP server.

    This is intentionally minimal: supports optional SSL/TLS and SMTP auth.
    Returns True on success, False on failure.
    """
    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = email
    msg["Subject"] = subject

    # Provide both plain-text and HTML alternatives
    try:
        plain = re.sub('<[^<]+?>', '', body)
    except Exception:
        plain = body
    msg.set_content(plain)
    msg.add_alternative(body, subtype="html")

    last_exc = None
    for attempt in range(1, MAIL_RETRIES + 2):
        try:
            if MAIL_USE_SSL:
                smtp = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, timeout=MAIL_TIMEOUT)
            else:
                smtp = smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=MAIL_TIMEOUT)

            with smtp:
                # STARTTLS if configured and not using SSL socket
                if (not MAIL_USE_SSL) and MAIL_USE_TLS:
                    smtp.starttls()

                # Login if credentials provided
                if MAIL_USERNAME and MAIL_PASSWORD:
                    try:
                        smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                    except Exception:
                        logger.exception("SMTP login failed")
                        raise

                smtp.send_message(msg)

            return True

        except Exception as exc:
            last_exc = exc
            logger.exception("Failed to send email (attempt %s): %s", attempt, exc)
            # simple backoff before retrying
            if attempt <= MAIL_RETRIES:
                time.sleep(1 + attempt)
            else:
                break

    # If we reach here, all attempts failed
    logger.error("Giving up sending email to %s after %s attempts: %s", email, MAIL_RETRIES + 1, last_exc)
    return False


def notificar_cambio_estado(caso_id: int, nombre_estado: str):
    db = SessionLocal()
    try:
        caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
        if not caso:
            return

        emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == caso.id_emprendedor).first()
        if emprendedor and emprendedor.email:
            # usar el nombre del caso cuando esté disponible
            caso_nombre = getattr(caso, 'nombre_caso', None) or str(caso_id)
            send_email(
                email=emprendedor.email,
                subject="Cambio de Estado de Caso",
                body=f"El estado del caso {caso_nombre} ha cambiado a <b>{nombre_estado}</b>."
            )
    finally:
        db.close()


def notificar_cambio_asignacion(asignacion_id: int):
    db = SessionLocal()
    try:
        asignacion = db.query(Asignacion).filter(Asignacion.id_asignacion == asignacion_id).first()
        if not asignacion:
            return

        caso = db.query(Caso).filter(Caso.id_caso == asignacion.id_caso).first()
        if not caso:
            return

        emprendedor = db.query(Emprendedor).filter(Emprendedor.id_emprendedor == caso.id_emprendedor).first()
        if emprendedor and emprendedor.email:
            # obtener datos del tutor y del caso para el cuerpo del correo
            tutor = db.query(Usuario).filter(Usuario.id_usuario == asignacion.id_usuario).first()
            tutor_name = None
            if tutor:
                tutor_name = tutor.nombre or ""
                if getattr(tutor, 'apellido', None):
                    tutor_name = f"{tutor_name} {tutor.apellido}".strip()

            caso_nombre = getattr(caso, 'nombre_caso', None) or f"{asignacion.id_caso}"

            tutor_display = tutor_name if tutor_name else "el tutor"

            send_email(
                email=emprendedor.email,
                subject="Asignación de Caso",
                body=f"Se ha asignado el tutor {tutor_display} al caso {caso_nombre}."
            )
    finally:
        db.close()