from datetime import date, time

from django.test import SimpleTestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.services.inscripcion_service import InscripcionService
from apps.inscripciones.tests.fakes import (
    FakeHorarioService,
    FakeInscripcionRepository,
    NotificadorEspia,
)
from apps.usuarios.models import Usuario


def participante(**cambios):
    return {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': '', **cambios}


class InscripcionServiceTests(SimpleTestCase):
    def setUp(self):
        self.usuario = Usuario(username='visitante', email='visitante@example.com')
        self.safari = Actividad(
            id=1, nombre='Safari', cupo_por_horario=20, requiere_talle=False, activa=True,
        )
        self.horario = Horario(
            id=10, actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.repository = FakeInscripcionRepository()
        self.notificador = NotificadorEspia()
        self.service = InscripcionService(
            inscripcion_repository=self.repository,
            horario_service=FakeHorarioService([self.horario]),
            notificador=self.notificador,
        )

    def solicitud(self, **cambios):
        return {
            'actividad_id': self.safari.id,
            'horario_id': self.horario.id,
            'acepta_terminos': True,
            'participantes': [participante()],
            **cambios,
        }

    def test_una_solicitud_valida_crea_la_inscripcion_con_sus_participantes(self):
        inscripcion = self.service.inscribir(self.usuario, self.solicitud())

        self.assertEqual(len(self.repository.creadas), 1)
        creada = self.repository.creadas[0]
        self.assertIs(creada['inscripcion'], inscripcion)
        self.assertEqual(inscripcion.usuario, self.usuario)
        self.assertEqual(inscripcion.horario, self.horario)
        self.assertTrue(inscripcion.acepta_terminos)
        self.assertEqual(creada['participantes'], [participante()])

    def test_una_inscripcion_valida_notifica_al_usuario(self):
        inscripcion = self.service.inscribir(self.usuario, self.solicitud())

        self.assertEqual(self.notificador.notificadas, [inscripcion])
