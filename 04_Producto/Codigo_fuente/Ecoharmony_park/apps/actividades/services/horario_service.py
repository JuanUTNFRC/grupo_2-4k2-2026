from apps.actividades.repositories.horario_repository import HorarioRepository


class HorarioService:
    """Puerta de entrada al dominio de actividades para consultar horarios."""

    def __init__(self, horario_repository=None):
        self.repository = horario_repository or HorarioRepository()

    def obtener(self, horario_id):
        return self.repository.obtener(horario_id)
