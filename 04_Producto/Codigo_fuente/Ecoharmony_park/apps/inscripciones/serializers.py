from rest_framework import serializers


class ParticipanteSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    dni = serializers.CharField()
    edad = serializers.IntegerField()
    talle = serializers.CharField()


class InscripcionCreateSerializer(serializers.Serializer):
    """Valida el formato de la solicitud. Las reglas de negocio las valida el service."""

    actividad_id = serializers.IntegerField()
    horario_id = serializers.IntegerField()
    acepta_terminos = serializers.BooleanField()
    participantes = ParticipanteSerializer(many=True)
