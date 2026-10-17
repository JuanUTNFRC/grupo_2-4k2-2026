from rest_framework import serializers

from apps.actividades.models import Actividad


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'nombre', 'requiere_talle', 'terminos_condiciones']
