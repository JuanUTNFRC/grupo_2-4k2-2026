from rest_framework.routers import DefaultRouter

from apps.actividades.views import ActividadViewSet

router = DefaultRouter()
router.register('actividades', ActividadViewSet, basename='actividad')

urlpatterns = router.urls
