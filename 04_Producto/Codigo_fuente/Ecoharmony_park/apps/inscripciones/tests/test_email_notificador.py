from datetime import date, time

from django.core import mail
from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.notificaciones.email_notificador import EmailNotificador
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.usuarios.models import Usuario


class EmailNotificadorTests(TestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        tirolesa = Actividad.objects.create(
            nombre='Tirolesa', cupo_por_horario=10, requiere_talle=True,
            terminos_condiciones='T&C',
        )
        horario = Horario.objects.create(
            actividad=tirolesa, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.inscripcion = InscripcionRepository().crear(
            usuario=usuario,
            horario=horario,
            acepta_terminos=True,
            participantes=[
                {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': 'M'},
                {'nombre': 'Juan Gómez', 'dni': '1234567', 'edad': 8, 'talle': 'XS'},
            ],
        )

    def test_envia_un_mail_al_usuario_con_actividad_fecha_y_hora_en_el_asunto(self):
        EmailNotificador().notificar(self.inscripcion)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['visitante@example.com'])
        self.assertEqual(
            mail.outbox[0].subject, 'Inscripción confirmada: Tirolesa - 13/10/2026 10:00',
        )
