from datetime import date, time

from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.usuarios.models import Usuario


def participante(**cambios):
    return {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': '', **cambios}


class InscripcionRepositoryTests(TestCase):
    def setUp(self):
        self.repository = InscripcionRepository()
        self.usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        self.safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )
        self.horario = Horario.objects.create(
            actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )

    def test_crear_guarda_la_inscripcion_con_sus_participantes(self):
        inscripcion = self.repository.crear(
            usuario=self.usuario,
            horario=self.horario,
            acepta_terminos=True,
            participantes=[participante(), participante(nombre='Juan', dni='1234567', talle='M')],
        )

        inscripcion.refresh_from_db()
        self.assertEqual(inscripcion.usuario, self.usuario)
        self.assertEqual(inscripcion.horario, self.horario)
        self.assertTrue(inscripcion.acepta_terminos)
        self.assertEqual(
            list(inscripcion.participantes.order_by('dni').values('nombre', 'dni', 'edad', 'talle')),
            [participante(nombre='Juan', dni='1234567', talle='M'), participante()],
        )
