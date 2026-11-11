from datetime import date, time

from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.actividades.services.horario_service import HorarioService


class HorarioServiceTests(TestCase):
    def test_obtener_devuelve_el_horario_guardado(self):
        safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )
        horario = Horario.objects.create(
            actividad=safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )

        self.assertEqual(HorarioService().obtener(horario.id), horario)

    def test_listar_devuelve_los_horarios_guardados_de_la_actividad(self):
        safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )
        horario = Horario.objects.create(
            actividad=safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )

        self.assertEqual(HorarioService().listar(safari.id, desde=date(2026, 10, 13)), [horario])
