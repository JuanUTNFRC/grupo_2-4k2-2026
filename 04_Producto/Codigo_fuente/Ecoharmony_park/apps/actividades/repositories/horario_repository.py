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
