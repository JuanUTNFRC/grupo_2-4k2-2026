from rest_framework.routers import DefaultRouter

from apps.inscripciones.views import InscripcionViewSet

router = DefaultRouter()
router.register('inscripciones', InscripcionViewSet, basename='inscripcion')

urlpatterns = router.urls
