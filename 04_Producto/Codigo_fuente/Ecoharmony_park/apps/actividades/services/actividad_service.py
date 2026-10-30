from apps.actividades.repositories.actividad_repository import ActividadRepository


class ActividadService:
    def __init__(self, actividad_repository=None):
        self.repository = actividad_repository or ActividadRepository()

    def listar_activas(self):
        return self.repository.listar_activas()
