import logging
from io import BytesIO

import segno
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class EmailNotificador:
    """Envía el mail de confirmación de la inscripción (RN7).

    Con silenciar_errores=False deja pasar los errores de envío, para que el
    worker de Celery los vea y reintente.
    """

    def __init__(self, silenciar_errores=True):
        self.silenciar_errores = silenciar_errores

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
        mensaje.attach(
            f'inscripcion_{inscripcion.codigo}.png', self._qr_png(inscripcion.codigo), 'image/png',
        )
        try:
            mensaje.send()
        except Exception:
            if not self.silenciar_errores:
                raise
            # La inscripción ya está confirmada: un mail caído no la invalida.
            # Queda registrado para reenviarlo.
            logger.exception('No se pudo enviar el mail de la inscripción %s', inscripcion.codigo)

    def _qr_png(self, codigo):
        buffer = BytesIO()
        segno.make(str(codigo), error='m').save(buffer, kind='png', scale=8)
        return buffer.getvalue()
