import logging

logger = logging.getLogger(__name__)


class ColaNotificador:
    """Encola el mail de confirmación para que lo envíe el worker de Celery.

    La inscripción responde sin esperar al servidor de mail.
    """

    def __init__(self, tarea):
        self.tarea = tarea

    def notificar(self, inscripcion):
        try:
            # Se encola el id y no el objeto: viaja como JSON y el worker
            # relee la inscripción de la base.
            self.tarea.delay(inscripcion.id)
        except Exception:
            # La inscripción ya está confirmada: si la cola no responde, el
            # mail queda registrado para reenviarlo.
            logger.exception('No se pudo encolar el mail de la inscripción %s', inscripcion.id)
