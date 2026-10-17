from rest_framework import status
from rest_framework.test import APITestCase

from apps.actividades.models import Actividad
from apps.usuarios.models import Usuario

URL = '/api/actividades/'


class ActividadApiTests(APITestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        self.client.force_authenticate(usuario)

    def test_lista_solo_las_actividades_activas_ordenadas_por_nombre(self):
        tirolesa = Actividad.objects.create(
            nombre='Tirolesa', cupo_por_horario=10, requiere_talle=True,
            terminos_condiciones='Usar arnés.',
        )
        safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='No bajar del vehículo.',
        )
        Actividad.objects.create(
            nombre='Palestra', cupo_por_horario=12, terminos_condiciones='T&C', activa=False,
        )

        respuesta = self.client.get(URL)

        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data, [
            {
                'id': safari.id, 'nombre': 'Safari', 'requiere_talle': False,
                'terminos_condiciones': 'No bajar del vehículo.',
            },
            {
                'id': tirolesa.id, 'nombre': 'Tirolesa', 'requiere_talle': True,
                'terminos_condiciones': 'Usar arnés.',
            },
        ])
