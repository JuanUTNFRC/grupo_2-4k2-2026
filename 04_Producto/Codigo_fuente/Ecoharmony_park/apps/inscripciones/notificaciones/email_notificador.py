from django.core.mail import EmailMessage


class EmailNotificador:
    """Envía el mail de confirmación de la inscripción (RN7)."""

    def notificar(self, inscripcion):
        horario = inscripcion.horario
        asunto = (
            f'Inscripción confirmada: {horario.actividad.nombre} - '
            f'{horario.fecha:%d/%m/%Y} {horario.hora_inicio:%H:%M}'
        )
        EmailMessage(subject=asunto, to=[inscripcion.usuario.email]).send()
