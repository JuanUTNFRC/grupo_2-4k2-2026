from rest_framework import serializers

from apps.inscripciones.models import Participante


class ParticipanteSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    dni = serializers.RegexField(r'^\d{7,8}$')
    edad = serializers.IntegerField(min_value=1)
    # Si el talle es obligatorio depende de la actividad: lo valida el service.
    talle = serializers.ChoiceField(
        choices=Participante.Talle.choices,
        allow_blank=True,
        default='',
    )


class InscripcionCreateSerializer(serializers.Serializer):
    """Valida el formato de la solicitud. Las reglas de negocio las valida el service."""

    actividad_id = serializers.IntegerField()
    horario_id = serializers.IntegerField()
    acepta_terminos = serializers.BooleanField()
    participantes = ParticipanteSerializer(many=True, allow_empty=False)
