from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailNotificador:
    """Envía el mail de confirmación de la inscripción (RN7)."""

    def notificar(self, inscripcion):
        horario = inscripcion.horario
        asunto = (
            f'Inscripción confirmada: {horario.actividad.nombre} - '
            f'{horario.fecha:%d/%m/%Y} {horario.hora_inicio:%H:%M}'
        )
        contexto = {
            'inscripcion': inscripcion,
            'horario': horario,
            'participantes': inscripcion.participantes.order_by('id'),
        }
        mensaje = EmailMultiAlternatives(
            subject=asunto,
            body=render_to_string('inscripciones/emails/confirmacion.txt', contexto),
            to=[inscripcion.usuario.email],
        )
        mensaje.attach_alternative(
            render_to_string('inscripciones/emails/confirmacion.html', contexto), 'text/html',
        )
        mensaje.send()
