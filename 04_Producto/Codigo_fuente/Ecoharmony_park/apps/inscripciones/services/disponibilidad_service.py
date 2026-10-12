from dataclasses import dataclass

from django.utils import timezone

from apps.actividades.models import Horario
from apps.actividades.services.calendario_service import CalendarioParqueService
from apps.actividades.services.horario_service import HorarioService
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository


@dataclass(frozen=True)
class HorarioDisponible:
    horario: Horario
    cupo_disponible: int


class DisponibilidadService:
    """Horarios de una actividad en los que todavía es posible inscribirse."""

    def __init__(
        self,
        horario_service=None,
        inscripcion_repository=None,
        calendario=None,
        reloj=timezone.now,
    ):
        # Sin argumentos usa las dependencias reales; los tests inyectan dobles.
        self.horarios = horario_service or HorarioService()
        self.inscripciones = inscripcion_repository or InscripcionRepository()
        self.calendario = calendario or CalendarioParqueService()
        self.reloj = reloj

    def horarios_disponibles(self, actividad_id):
        ahora = self.reloj()
        horarios = [
            horario
            for horario in self.horarios.listar(actividad_id, desde=timezone.localdate(ahora))
            if self._admite_inscripciones(horario, ahora)
        ]
        ocupados = self.inscripciones.participantes_por_horario([h.id for h in horarios])
        disponibles = [
            HorarioDisponible(horario, horario.actividad.cupo_por_horario - ocupados[horario.id])
            for horario in horarios
        ]
        return [d for d in disponibles if d.cupo_disponible > 0]

    def _admite_inscripciones(self, horario, ahora):
        """Actividad activa, horario sin comenzar y con el parque abierto."""
        return (
            horario.actividad.activa
            and horario.inicio > ahora
            and self.calendario.admite_actividad(horario.fecha, horario.hora_inicio)
        )
