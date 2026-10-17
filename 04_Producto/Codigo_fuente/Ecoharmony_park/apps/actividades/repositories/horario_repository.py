from apps.actividades.models import Horario


class HorarioRepository:
    def obtener(self, horario_id):
        """Horario con su actividad cargada, o None si no existe."""
        return (
            Horario.objects
            .select_related('actividad')
            .filter(id=horario_id)
            .first()
        )

    def listar(self, actividad_id, desde):
        """Horarios de la actividad desde una fecha, ordenados y con su actividad cargada."""
        return list(
            Horario.objects
            .select_related('actividad')
            .filter(actividad_id=actividad_id, fecha__gte=desde)
            .order_by('fecha', 'hora_inicio')
        )
