from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.actividades.serializers import ActividadSerializer
from apps.actividades.services.actividad_service import ActividadService


class ActividadViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        actividades = ActividadService().listar_activas()
        return Response(ActividadSerializer(actividades, many=True).data)
