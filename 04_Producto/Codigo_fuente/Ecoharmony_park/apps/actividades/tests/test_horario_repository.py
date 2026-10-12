from datetime import date, time

from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.actividades.repositories.horario_repository import HorarioRepository


class HorarioRepositoryTests(TestCase):
    def setUp(self):
        self.repository = HorarioRepository()
        self.safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )
        self.horario = Horario.objects.create(
            actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )

    def test_obtener_devuelve_el_horario_con_su_actividad_en_una_sola_query(self):
        with self.assertNumQueries(1):
            horario = self.repository.obtener(self.horario.id)
            self.assertEqual(horario.actividad.nombre, 'Safari')

        self.assertEqual(horario, self.horario)

    def test_obtener_un_horario_inexistente_devuelve_none(self):
        self.assertIsNone(self.repository.obtener(999))
