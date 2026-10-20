from datetime import date, time

from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.inscripciones.tests.helpers import participante
from apps.usuarios.models import Usuario


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

    def inscribir(self, horario, *dnis):
        return self.repository.crear(
            usuario=self.usuario,
            horario=horario,
            acepta_terminos=True,
            participantes=[participante(dni=dni) for dni in dnis],
        )

    def test_participantes_inscriptos_suma_los_de_todas_las_inscripciones_del_horario(self):
        otro_horario = Horario.objects.create(
            actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(11, 0),
        )
        self.inscribir(self.horario, '30000001', '30000002')
        self.inscribir(self.horario, '30000003')
        self.inscribir(otro_horario, '30000004')

        self.assertEqual(self.repository.participantes_inscriptos(self.horario.id), 3)

    def test_participantes_inscriptos_de_un_horario_sin_inscripciones_es_0(self):
        self.assertEqual(self.repository.participantes_inscriptos(self.horario.id), 0)

    def test_dnis_inscriptos_devuelve_los_dnis_del_horario(self):
        otro_horario = Horario.objects.create(
            actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(11, 0),
        )
        self.inscribir(self.horario, '30000001', '30000002')
        self.inscribir(self.horario, '30000003')
        self.inscribir(otro_horario, '30000004')

        self.assertEqual(
            self.repository.dnis_inscriptos(self.horario.id),
            {'30000001', '30000002', '30000003'},
        )

    def test_dnis_inscriptos_a_la_misma_hora_incluye_las_otras_actividades(self):
        tirolesa = Actividad.objects.create(
            nombre='Tirolesa', cupo_por_horario=10, requiere_talle=True, terminos_condiciones='T&C',
        )
        misma_hora = Horario.objects.create(
            actividad=tirolesa, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        otra_hora = Horario.objects.create(
            actividad=tirolesa, fecha=date(2026, 10, 13), hora_inicio=time(11, 0),
        )
        otro_dia = Horario.objects.create(
            actividad=tirolesa, fecha=date(2026, 10, 14), hora_inicio=time(10, 0),
        )
        self.inscribir(self.horario, '30000001')
        self.inscribir(misma_hora, '30000002')
        self.inscribir(otra_hora, '30000003')
        self.inscribir(otro_dia, '30000004')

        self.assertEqual(
            self.repository.dnis_inscriptos_a_la_misma_hora(self.horario),
            {'30000001', '30000002'},
        )

    def test_bloquear_horario_revierte_lo_creado_si_falla_adentro(self):
        with self.assertRaises(RuntimeError):
            with self.repository.bloquear_horario(self.horario.id):
                self.inscribir(self.horario, '30000001')
                raise RuntimeError('falla después de crear')

        self.assertEqual(self.repository.participantes_inscriptos(self.horario.id), 0)

    def test_bloquear_horario_confirma_lo_creado_si_no_falla(self):
        with self.repository.bloquear_horario(self.horario.id):
            self.inscribir(self.horario, '30000001')

        self.assertEqual(self.repository.participantes_inscriptos(self.horario.id), 1)

    def test_participantes_por_horario_cuenta_cada_horario_en_una_sola_query(self):
        con_dos = self.horario
        con_uno = Horario.objects.create(
            actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(11, 0),
        )
        vacio = Horario.objects.create(
            actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(12, 0),
        )
        self.inscribir(con_dos, '30000001', '30000002')
        self.inscribir(con_uno, '30000003')

        with self.assertNumQueries(1):
            ocupados = self.repository.participantes_por_horario([con_dos.id, con_uno.id, vacio.id])

        self.assertEqual(ocupados, {con_dos.id: 2, con_uno.id: 1, vacio.id: 0})
