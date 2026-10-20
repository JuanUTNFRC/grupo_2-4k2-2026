from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase

from apps.actividades.models import Actividad, Horario
from apps.actividades.services.calendario_service import CalendarioParqueService
from apps.inscripciones.exceptions.inscripcion_exceptions import (
    CupoInsuficienteError,
    DniDuplicadoError,
    EdadMinimaError,
    HorarioNoDisponibleError,
    InscripcionCerradaError,
    InscripcionNoHabilitadaError,
    ParqueCerradoError,
    TalleRequeridoError,
    TerminosNoAceptadosError,
)
from apps.inscripciones.services.inscripcion_service import InscripcionService
from apps.inscripciones.tests.fakes import (
    FakeHorarioService,
    FakeInscripcionRepository,
    NotificadorEspia,
)
from apps.inscripciones.tests.helpers import participante
from apps.usuarios.models import Usuario


CORDOBA = ZoneInfo('America/Argentina/Cordoba')


class InscripcionServiceTests(SimpleTestCase):
    def setUp(self):
        self.usuario = Usuario(username='visitante', email='visitante@example.com')
        self.safari = Actividad(
            id=1, nombre='Safari', cupo_por_horario=20, requiere_talle=False, activa=True,
        )
        self.horario = Horario(
            id=10, actividad=self.safari, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.tirolesa = Actividad(
            id=2, nombre='Tirolesa', cupo_por_horario=10, requiere_talle=True, edad_minima=8,
            activa=True,
        )
        self.horario_tirolesa = Horario(
            id=20, actividad=self.tirolesa, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.horario_service = FakeHorarioService([self.horario, self.horario_tirolesa])
        self.repository = FakeInscripcionRepository()
        self.notificador = NotificadorEspia()
        self.service = InscripcionService(
            inscripcion_repository=self.repository,
            horario_service=self.horario_service,
            notificador=self.notificador,
            calendario=CalendarioParqueService(),
            reloj=lambda: self.ahora,
        )
        # Antes de todos los horarios del setUp, salvo que el test lo cambie.
        self.ahora = datetime(2026, 10, 13, 8, 0, tzinfo=CORDOBA)

    def solicitud(self, **cambios):
        return {
            'actividad_id': self.safari.id,
            'horario_id': self.horario.id,
            'acepta_terminos': True,
            'participantes': [participante()],
            **cambios,
        }

    def assertRechazada(self, excepcion, solicitud):
        """Falla con `excepcion`, sin guardar ni notificar nada (RN7)."""
        with self.assertRaises(excepcion):
            self.service.inscribir(self.usuario, solicitud)

        self.assertEqual(self.repository.creadas, [])
        self.assertEqual(self.notificador.notificadas, [])

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

    def test_un_horario_sin_cupo_rechaza_la_inscripcion(self):
        self.repository.ocupados[self.horario.id] = self.safari.cupo_por_horario

        self.assertRechazada(CupoInsuficienteError, self.solicitud())

    def test_mas_participantes_que_el_cupo_restante_rechaza_la_inscripcion(self):
        self.repository.ocupados[self.horario.id] = self.safari.cupo_por_horario - 2
        grupo = [participante(dni=dni) for dni in ['30000001', '30000002', '30000003']]

        self.assertRechazada(CupoInsuficienteError, self.solicitud(participantes=grupo))

    def test_completar_exactamente_el_cupo_restante_es_valido(self):
        self.repository.ocupados[self.horario.id] = self.safari.cupo_por_horario - 2
        grupo = [participante(dni=dni) for dni in ['30000001', '30000002']]

        self.service.inscribir(self.usuario, self.solicitud(participantes=grupo))

        self.assertEqual(len(self.repository.creadas), 1)

    def test_sin_talle_en_una_actividad_que_no_lo_requiere_es_valido(self):
        self.service.inscribir(self.usuario, self.solicitud(participantes=[participante(talle='')]))

        self.assertEqual(len(self.repository.creadas), 1)

    def test_sin_talle_en_una_actividad_que_lo_requiere_rechaza_la_inscripcion(self):
        solicitud = self.solicitud(
            actividad_id=self.tirolesa.id,
            horario_id=self.horario_tirolesa.id,
            participantes=[participante(talle='M'), participante(dni='30000002', talle='')],
        )

        self.assertRechazada(TalleRequeridoError, solicitud)

    def solicitud_tirolesa(self, *participantes):
        return self.solicitud(
            actividad_id=self.tirolesa.id,
            horario_id=self.horario_tirolesa.id,
            participantes=list(participantes),
        )

    def test_un_participante_menor_a_la_edad_minima_rechaza_la_inscripcion(self):
        solicitud = self.solicitud_tirolesa(
            participante(talle='M'), participante(dni='30000002', edad=7, talle='S'),
        )

        self.assertRechazada(EdadMinimaError, solicitud)

    def test_un_participante_con_la_edad_minima_justa_es_valido(self):
        self.service.inscribir(self.usuario, self.solicitud_tirolesa(participante(edad=8, talle='S')))

        self.assertEqual(len(self.repository.creadas), 1)

    def test_una_actividad_sin_edad_minima_admite_cualquier_edad(self):
        self.service.inscribir(self.usuario, self.solicitud(participantes=[participante(edad=1)]))

        self.assertEqual(len(self.repository.creadas), 1)

    def test_sin_aceptar_los_terminos_y_condiciones_rechaza_la_inscripcion(self):
        self.assertRechazada(TerminosNoAceptadosError, self.solicitud(acepta_terminos=False))

    def test_un_horario_con_el_parque_cerrado_rechaza_la_inscripcion(self):
        lunes = date(2026, 10, 19)
        horario_lunes = Horario(id=30, actividad=self.safari, fecha=lunes, hora_inicio=time(10, 0))
        self.horario_service.horarios[horario_lunes.id] = horario_lunes

        self.assertRechazada(ParqueCerradoError, self.solicitud(horario_id=horario_lunes.id))

    def test_un_horario_inexistente_rechaza_la_inscripcion(self):
        self.assertRechazada(HorarioNoDisponibleError, self.solicitud(horario_id=999))

    def test_un_horario_de_otra_actividad_rechaza_la_inscripcion(self):
        solicitud = self.solicitud(actividad_id=self.safari.id, horario_id=self.horario_tirolesa.id)

        self.assertRechazada(HorarioNoDisponibleError, solicitud)

    def test_una_actividad_inactiva_rechaza_la_inscripcion(self):
        self.safari.activa = False

        self.assertRechazada(HorarioNoDisponibleError, self.solicitud())

    def test_un_horario_que_ya_comenzo_rechaza_la_inscripcion(self):
        self.ahora = datetime(2026, 10, 13, 10, 0, tzinfo=CORDOBA)

        self.assertRechazada(InscripcionCerradaError, self.solicitud())

    def test_inscribirse_15_minutos_antes_del_horario_rechaza_la_inscripcion(self):
        self.ahora = datetime(2026, 10, 13, 9, 45, tzinfo=CORDOBA)

        self.assertRechazada(InscripcionCerradaError, self.solicitud())

    def test_inscribirse_16_minutos_antes_del_horario_es_valido(self):
        self.ahora = datetime(2026, 10, 13, 9, 44, tzinfo=CORDOBA)

        self.service.inscribir(self.usuario, self.solicitud())

        self.assertEqual(len(self.repository.creadas), 1)

    def test_un_horario_que_empieza_en_mas_de_24_horas_rechaza_la_inscripcion(self):
        self.ahora = datetime(2026, 10, 12, 9, 59, tzinfo=CORDOBA)

        self.assertRechazada(InscripcionNoHabilitadaError, self.solicitud())

    def test_inscribirse_justo_24_horas_antes_del_horario_es_valido(self):
        self.ahora = datetime(2026, 10, 12, 10, 0, tzinfo=CORDOBA)

        self.service.inscribir(self.usuario, self.solicitud())

        self.assertEqual(len(self.repository.creadas), 1)

    def test_un_dni_repetido_en_la_solicitud_rechaza_la_inscripcion(self):
        grupo = [participante(dni='30123456'), participante(nombre='Otra', dni='30123456')]

        self.assertRechazada(DniDuplicadoError, self.solicitud(participantes=grupo))

    def test_un_dni_ya_inscripto_en_el_horario_rechaza_la_inscripcion(self):
        self.repository.dnis[self.horario.id] = {'30123456'}

        self.assertRechazada(
            DniDuplicadoError, self.solicitud(participantes=[participante(dni='30123456')]),
        )

    def test_un_dni_inscripto_en_otro_horario_es_valido(self):
        self.repository.dnis[self.horario_tirolesa.id] = {'30123456'}

        self.service.inscribir(self.usuario, self.solicitud(participantes=[participante(dni='30123456')]))

        self.assertEqual(len(self.repository.creadas), 1)
