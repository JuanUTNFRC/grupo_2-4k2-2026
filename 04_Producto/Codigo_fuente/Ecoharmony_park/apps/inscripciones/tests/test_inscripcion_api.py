from datetime import time, timedelta

from django.core import mail
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.actividades.models import Actividad, Horario
from apps.usuarios.models import Usuario

URL = '/api/inscripciones/'


def proximo_martes():
    hoy = timezone.localdate()
    return hoy + timedelta(days=(1 - hoy.weekday()) % 7 or 7)


def participante(**cambios):
    return {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': '', **cambios}


class InscripcionApiTests(APITestCase):
    """Pruebas de usuario PU1 a PU6 de punta a punta por HTTP."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        self.client.force_authenticate(self.usuario)
        self.tirolesa = Actividad.objects.create(
            nombre='Tirolesa', cupo_por_horario=10, requiere_talle=True,
            terminos_condiciones='T&C',
        )
        self.horario_tirolesa = Horario.objects.create(
            actividad=self.tirolesa, fecha=proximo_martes(), hora_inicio=time(10, 0),
        )

    def solicitud(self, actividad, horario, **cambios):
        return {
            'actividad_id': actividad.id,
            'horario_id': horario.id,
            'acepta_terminos': True,
            'participantes': [participante(talle='M')],
            **cambios,
        }

    def test_pu1_inscripcion_valida_con_talle_responde_201_y_envia_el_mail(self):
        respuesta = self.client.post(
            URL, self.solicitud(self.tirolesa, self.horario_tirolesa), format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(respuesta.data['actividad'], 'Tirolesa')
        self.assertEqual(respuesta.data['participantes'], [participante(talle='M')])
        self.assertEqual(len(mail.outbox), 1)
