from rest_framework import serializers


class ParticipanteSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    dni = serializers.RegexField(r'^\d{7,8}$')
    edad = serializers.IntegerField(min_value=1)
    talle = serializers.CharField()


class InscripcionCreateSerializer(serializers.Serializer):
    """Valida el formato de la solicitud. Las reglas de negocio las valida el service."""

    actividad_id = serializers.IntegerField()
    horario_id = serializers.IntegerField()
    acepta_terminos = serializers.BooleanField()
    participantes = ParticipanteSerializer(many=True, allow_empty=False)
