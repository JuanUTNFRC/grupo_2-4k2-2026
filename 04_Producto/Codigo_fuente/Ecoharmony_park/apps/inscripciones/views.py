from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.inscripciones.serializers import InscripcionCreateSerializer, InscripcionSerializer
from apps.inscripciones.services.inscripcion_service import InscripcionService


class InscripcionViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        entrada = InscripcionCreateSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        inscripcion = InscripcionService().inscribir(request.user, entrada.validated_data)
        return Response(InscripcionSerializer(inscripcion).data, status=status.HTTP_201_CREATED)
