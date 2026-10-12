from datetime import time

from django.core import mail
from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.models import Inscripcion
from apps.inscripciones.services.inscripcion_service import InscripcionService
from apps.inscripciones.tests.helpers import proximo_martes
from apps.usuarios.models import Usuario


class InscripcionIntegracionTests(TestCase):
    """PU1 de punta a punta con las dependencias reales del service."""

    def test_una_inscripcion_valida_se_guarda_y_envia_el_mail(self):
        usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )
        horario = Horario.objects.create(
            actividad=safari, fecha=proximo_martes(), hora_inicio=time(10, 0),
        )

        InscripcionService().inscribir(usuario, {
            'actividad_id': safari.id,
            'horario_id': horario.id,
            'acepta_terminos': True,
            'participantes': [{'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': ''}],
        })

        self.assertEqual(Inscripcion.objects.filter(usuario=usuario, horario=horario).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
