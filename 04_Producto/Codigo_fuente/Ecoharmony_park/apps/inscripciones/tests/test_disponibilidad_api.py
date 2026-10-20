from datetime import time

from rest_framework import status
from rest_framework.test import APITestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.inscripciones.tests.helpers import MARTES, fijar_reloj, participante
from apps.usuarios.models import Usuario

URL = '/api/horarios-disponibles/'


class HorariosDisponiblesApiTests(APITestCase):
    def setUp(self):
        fijar_reloj(self)
        self.usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        self.client.force_authenticate(self.usuario)
        self.safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )

    def test_lista_los_horarios_disponibles_con_su_cupo(self):
        horario = Horario.objects.create(actividad=self.safari, fecha=MARTES, hora_inicio=time(10, 0))
        InscripcionRepository().crear(
            usuario=self.usuario, horario=horario, acepta_terminos=True,
            participantes=[participante(dni='30000001'), participante(dni='30000002')],
        )

        respuesta = self.client.get(URL, {'actividad_id': self.safari.id})

        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data, [{
            'id': horario.id,
            'fecha': MARTES.isoformat(),
            'hora_inicio': '10:00',
            'cupo_disponible': 18,
        }])

    def test_sin_actividad_id_responde_400(self):
        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respuesta.data['codigo'], 'datos_invalidos')
