from smtplib import SMTPException

from celery import shared_task

from apps.inscripciones.notificaciones.email_notificador import EmailNotificador
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository


# Reintenta ante fallas del servidor de mail (SMTP) o de red (OSError), con
# espera creciente entre intentos.
@shared_task(
    autoretry_for=(SMTPException, OSError),
    retry_backoff=True,
    max_retries=3,
)
def enviar_mail_confirmacion(inscripcion_id):
    inscripcion = InscripcionRepository().obtener(inscripcion_id)
    EmailNotificador(silenciar_errores=False).notificar(inscripcion)
