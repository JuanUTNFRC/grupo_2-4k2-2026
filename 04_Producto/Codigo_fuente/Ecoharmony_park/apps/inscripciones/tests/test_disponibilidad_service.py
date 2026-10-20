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

    def agregar_horario(self, id, fecha=date(2026, 10, 13), hora_inicio=time(11, 0), actividad=None):
        horario = Horario(
            id=id, actividad=actividad or self.safari, fecha=fecha, hora_inicio=hora_inicio,
        )
        self.horario_service.horarios[id] = horario
        return horario

    def horarios_listados(self):
        return [d.horario for d in self.service.horarios_disponibles(self.safari.id)]

    def test_lista_los_horarios_de_la_actividad_con_su_cupo_disponible(self):
        self.repository.ocupados[self.horario.id] = 5

        disponibles = self.service.horarios_disponibles(self.safari.id)

        self.assertEqual(len(disponibles), 1)
        self.assertEqual(disponibles[0].horario, self.horario)
        self.assertEqual(disponibles[0].cupo_disponible, 15)

    def test_excluye_los_horarios_sin_cupo(self):
        lleno = self.agregar_horario(11)
        self.repository.ocupados[lleno.id] = self.safari.cupo_por_horario

        self.assertEqual(self.horarios_listados(), [self.horario])

    def test_excluye_los_horarios_que_ya_comenzaron(self):
        siguiente = self.agregar_horario(11, hora_inicio=time(11, 0))
        self.ahora = datetime(2026, 10, 13, 10, 0, tzinfo=CORDOBA)

        self.assertEqual(self.horarios_listados(), [siguiente])

    def test_excluye_los_horarios_que_empiezan_en_15_minutos_o_menos(self):
        siguiente = self.agregar_horario(11, hora_inicio=time(11, 0))
        self.ahora = datetime(2026, 10, 13, 9, 45, tzinfo=CORDOBA)

        self.assertEqual(self.horarios_listados(), [siguiente])

    def test_excluye_los_horarios_que_empiezan_en_mas_de_24_horas(self):
        self.ahora = datetime(2026, 10, 13, 9, 0, tzinfo=CORDOBA)
        justo_24_horas = self.agregar_horario(11, fecha=date(2026, 10, 14), hora_inicio=time(9, 0))
        self.agregar_horario(12, fecha=date(2026, 10, 14), hora_inicio=time(10, 0))

        self.assertEqual(self.horarios_listados(), [self.horario, justo_24_horas])

    def test_excluye_los_horarios_con_el_parque_cerrado(self):
        lunes = date(2026, 10, 19)
        self.agregar_horario(11, fecha=lunes)

        self.assertEqual(self.horarios_listados(), [self.horario])

    def test_una_actividad_inactiva_no_tiene_horarios_disponibles(self):
        self.safari.activa = False

        self.assertEqual(self.horarios_listados(), [])
