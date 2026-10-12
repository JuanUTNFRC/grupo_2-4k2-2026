class ColaNotificador:
    """Encola el mail de confirmación para que lo envíe el worker de Celery.

    La inscripción responde sin esperar al servidor de mail.
    """

    def __init__(self, tarea):
        self.tarea = tarea

    def notificar(self, inscripcion):
        # Se encola el id y no el objeto: viaja como JSON y el worker relee
        # la inscripción de la base.
        self.tarea.delay(inscripcion.id)
