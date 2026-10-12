from datetime import date, time
from smtplib import SMTPException
from unittest.mock import patch

from django.core import mail
from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.inscripciones.tasks import enviar_mail_confirmacion
from apps.inscripciones.tests.helpers import participante
from apps.usuarios.models import Usuario


class EnviarMailConfirmacionTests(TestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )
        horario = Horario.objects.create(
            actividad=safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.inscripcion = InscripcionRepository().crear(
            usuario=usuario, horario=horario, acepta_terminos=True,
            participantes=[participante()],
        )

    def test_envia_el_mail_de_la_inscripcion(self):
        enviar_mail_confirmacion(self.inscripcion.id)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['visitante@example.com'])
        self.assertIn(str(self.inscripcion.codigo), mail.outbox[0].body)

    def test_si_falla_el_smtp_reintenta_el_envio(self):
        with patch(
            'django.core.mail.EmailMultiAlternatives.send', side_effect=SMTPException('caído'),
        ) as send:
            resultado = enviar_mail_confirmacion.apply(args=[self.inscripcion.id])

        self.assertTrue(resultado.failed())
        self.assertEqual(send.call_count, 1 + enviar_mail_confirmacion.max_retries)
