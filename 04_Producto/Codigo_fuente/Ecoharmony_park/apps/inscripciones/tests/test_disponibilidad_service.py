from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase

from apps.actividades.models import Actividad, Horario
from apps.actividades.services.calendario_service import CalendarioParqueService
from apps.inscripciones.services.disponibilidad_service import DisponibilidadService
from apps.inscripciones.tests.fakes import FakeHorarioService, FakeInscripcionRepository

CORDOBA = ZoneInfo('America/Argentina/Cordoba')


class DisponibilidadServiceTests(SimpleTestCase):
    def setUp(self):
        self.safari = Actividad(
            id=1, nombre='Safari', cupo_por_horario=20, requiere_talle=False, activa=True,
        )
        self.horario = Horario(
            id=10, actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.horario_service = FakeHorarioService([self.horario])
        self.repository = FakeInscripcionRepository()
        self.ahora = datetime(2026, 10, 13, 8, 0, tzinfo=CORDOBA)
        self.service = DisponibilidadService(
            horario_service=self.horario_service,
            inscripcion_repository=self.repository,
            calendario=CalendarioParqueService(),
            reloj=lambda: self.ahora,
        )

    def test_lista_los_horarios_de_la_actividad_con_su_cupo_disponible(self):
        self.repository.ocupados[self.horario.id] = 5

        disponibles = self.service.horarios_disponibles(self.safari.id)

        self.assertEqual(len(disponibles), 1)
        self.assertEqual(disponibles[0].horario, self.horario)
        self.assertEqual(disponibles[0].cupo_disponible, 15)
