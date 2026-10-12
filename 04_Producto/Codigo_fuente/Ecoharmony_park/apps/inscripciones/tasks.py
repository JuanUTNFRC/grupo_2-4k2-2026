from celery import shared_task

from apps.inscripciones.notificaciones.email_notificador import EmailNotificador
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository


@shared_task
def enviar_mail_confirmacion(inscripcion_id):
    inscripcion = InscripcionRepository().obtener(inscripcion_id)
    EmailNotificador().notificar(inscripcion)
