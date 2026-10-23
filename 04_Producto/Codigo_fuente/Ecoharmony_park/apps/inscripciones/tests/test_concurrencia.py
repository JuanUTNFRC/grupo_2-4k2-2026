import threading
import time as reloj_sistema
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from django.db import connection
from django.test import TransactionTestCase

from apps.actividades.models import Actividad, Horario
from apps.actividades.services.calendario_service import CalendarioParqueService
from apps.actividades.services.horario_service import HorarioService
from apps.inscripciones.exceptions.inscripcion_exceptions import CupoInsuficienteError
from apps.inscripciones.models import Participante
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.inscripciones.services.inscripcion_service import InscripcionService
from apps.inscripciones.tests.fakes import NotificadorEspia
from apps.usuarios.models import Usuario


class InscripcionRepositoryLento(InscripcionRepository):
    """Demora después de contar el cupo, para que las dos inscripciones se crucen."""

    def participantes_inscriptos(self, horario_id):
        ocupados = super().participantes_inscriptos(horario_id)
        reloj_sistema.sleep(0.2)
        return ocupados


class InscripcionConcurrenteTests(TransactionTestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        ultimo_lugar = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=1, terminos_condiciones='T&C',
        )
        self.horario = Horario.objects.create(
            actividad=ultimo_lugar, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.service = InscripcionService(
            inscripcion_repository=InscripcionRepositoryLento(),
            horario_service=HorarioService(),
            notificador=NotificadorEspia(),
            calendario=CalendarioParqueService(),
            reloj=lambda: datetime(2026, 10, 13, 8, 0, tzinfo=ZoneInfo('America/Argentina/Cordoba')),
        )

    def inscribir_en_paralelo(self, dni, largada, resultados):
        datos = {
            'actividad_id': self.horario.actividad_id,
            'horario_id': self.horario.id,
            'acepta_terminos': True,
            'participantes': [{'nombre': 'Ana', 'dni': dni, 'edad': 30, 'talle': ''}],
        }
        try:
            largada.wait()
            self.service.inscribir(self.usuario, datos)
            resultados.append('inscripta')
        except CupoInsuficienteError:
            resultados.append('sin cupo')
        finally:
            connection.close()  # cada hilo usa su propia conexión

    def test_dos_inscripciones_simultaneas_no_superan_el_cupo(self):
        largada = threading.Barrier(2)
        resultados = []
        hilos = [
            threading.Thread(target=self.inscribir_en_paralelo, args=(dni, largada, resultados))
            for dni in ['30000001', '30000002']
        ]
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()

        self.assertEqual(sorted(resultados), ['inscripta', 'sin cupo'])
        self.assertEqual(Participante.objects.filter(inscripcion__horario=self.horario).count(), 1)
