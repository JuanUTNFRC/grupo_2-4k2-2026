from django.utils import timezone

from apps.actividades.services.calendario_service import CalendarioParqueService
from apps.actividades.services.horario_service import HorarioService
from apps.inscripciones.exceptions.inscripcion_exceptions import (
    CupoInsuficienteError,
    DniDuplicadoError,
    HorarioNoDisponibleError,
    ParqueCerradoError,
    TalleRequeridoError,
    TerminosNoAceptadosError,
)
from apps.inscripciones.notificaciones.cola_notificador import ColaNotificador
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository


class InscripcionService:
    """Reglas de negocio de la inscripción a una actividad.

    Recibe datos ya validados en formato por InscripcionCreateSerializer.
    """

    def __init__(
        self,
        inscripcion_repository=None,
        horario_service=None,
        notificador=None,
        calendario=None,
        reloj=timezone.now,
    ):
        # Sin argumentos usa las dependencias reales; los tests inyectan dobles.
        self.inscripciones = inscripcion_repository or InscripcionRepository()
        self.horarios = horario_service or HorarioService()
        self.notificador = notificador or ColaNotificador()
        self.calendario = calendario or CalendarioParqueService()
        self.reloj = reloj

    def inscribir(self, usuario, datos):
        participantes = datos['participantes']
        horario = self._obtener_horario_disponible(datos['actividad_id'], datos['horario_id'])
        if not self.calendario.admite_actividad(horario.fecha, horario.hora_inicio):
            raise ParqueCerradoError()
        if not datos['acepta_terminos']:
            raise TerminosNoAceptadosError()
        self._validar_talles(horario.actividad, participantes)

        # DNI y cupo se validan y se ocupan con el horario bloqueado, para que
        # dos inscripciones simultáneas no tomen el mismo lugar.
        with self.inscripciones.bloquear_horario(horario.id):
            self._validar_dnis(horario, participantes)
            self._validar_cupo(horario, participantes)
            inscripcion = self.inscripciones.crear(
                usuario=usuario,
                horario=horario,
                acepta_terminos=datos['acepta_terminos'],
                participantes=participantes,
            )

        self.notificador.notificar(inscripcion)
        return inscripcion

    def _obtener_horario_disponible(self, actividad_id, horario_id):
        horario = self.horarios.obtener(horario_id)
        if (
            horario is None
            or horario.actividad_id != actividad_id
            or not horario.actividad.activa
            or self._ya_comenzo(horario)
        ):
            raise HorarioNoDisponibleError()
        return horario

    def _ya_comenzo(self, horario):
        return horario.inicio <= self.reloj()

    def _validar_talles(self, actividad, participantes):
        if actividad.requiere_talle and any(not p['talle'] for p in participantes):
            raise TalleRequeridoError()

    def _validar_dnis(self, horario, participantes):
        dnis = [p['dni'] for p in participantes]
        repetidos_en_solicitud = len(dnis) != len(set(dnis))
        ya_inscriptos = self.inscripciones.dnis_inscriptos(horario.id) & set(dnis)
        if repetidos_en_solicitud or ya_inscriptos:
            raise DniDuplicadoError()

    def _validar_cupo(self, horario, participantes):
        ocupados = self.inscripciones.participantes_inscriptos(horario.id)
        disponibles = horario.actividad.cupo_por_horario - ocupados
        if len(participantes) > disponibles:
            raise CupoInsuficienteError()
