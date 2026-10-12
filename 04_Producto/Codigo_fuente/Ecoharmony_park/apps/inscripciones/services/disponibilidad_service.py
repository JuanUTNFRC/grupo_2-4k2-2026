from dataclasses import dataclass

from django.utils import timezone

from apps.actividades.models import Horario


@dataclass(frozen=True)
class HorarioDisponible:
    horario: Horario
    cupo_disponible: int


class DisponibilidadService:
    """Horarios de una actividad en los que todavía es posible inscribirse."""

    def __init__(self, horario_service, inscripcion_repository, calendario, reloj):
        self.horarios = horario_service
        self.inscripciones = inscripcion_repository
        self.calendario = calendario
        self.reloj = reloj

    def horarios_disponibles(self, actividad_id):
        hoy = timezone.localdate(self.reloj())
        horarios = self.horarios.listar(actividad_id, desde=hoy)
        ocupados = self.inscripciones.participantes_por_horario([h.id for h in horarios])
        disponibles = [
            HorarioDisponible(horario, horario.actividad.cupo_por_horario - ocupados[horario.id])
            for horario in horarios
        ]
        ahora = self.reloj()
        return [
            d for d in disponibles
            if d.cupo_disponible > 0
            and d.horario.inicio > ahora
            and self.calendario.admite_actividad(d.horario.fecha, d.horario.hora_inicio)
        ]
