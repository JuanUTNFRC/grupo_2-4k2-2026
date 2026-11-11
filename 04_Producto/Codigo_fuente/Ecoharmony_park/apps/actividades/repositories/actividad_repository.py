from apps.actividades.models import Actividad


class ActividadRepository:
    def listar_activas(self):
        return list(Actividad.objects.filter(activa=True).order_by('nombre'))
