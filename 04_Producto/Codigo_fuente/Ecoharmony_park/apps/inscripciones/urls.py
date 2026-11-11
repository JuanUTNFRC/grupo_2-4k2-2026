from rest_framework.routers import DefaultRouter

from apps.inscripciones.views import HorarioDisponibleViewSet, InscripcionViewSet

router = DefaultRouter()
router.register('inscripciones', InscripcionViewSet, basename='inscripcion')
router.register('horarios-disponibles', HorarioDisponibleViewSet, basename='horario-disponible')

urlpatterns = router.urls
