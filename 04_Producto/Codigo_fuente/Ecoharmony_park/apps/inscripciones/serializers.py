from rest_framework import serializers

from apps.inscripciones.models import Inscripcion, Participante


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


class ParticipanteSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ['nombre', 'dni', 'edad', 'talle']


class InscripcionSerializer(serializers.ModelSerializer):
    """Representación de una inscripción creada."""

    actividad = serializers.CharField(source='horario.actividad.nombre')
    fecha = serializers.DateField(source='horario.fecha')
    hora_inicio = serializers.TimeField(source='horario.hora_inicio', format='%H:%M')
    participantes = ParticipanteSalidaSerializer(many=True)

    class Meta:
        model = Inscripcion
        fields = ['codigo', 'actividad', 'fecha', 'hora_inicio', 'participantes', 'creada_en']


class HorariosDisponiblesQuerySerializer(serializers.Serializer):
    actividad_id = serializers.IntegerField()


class HorarioDisponibleSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='horario.id')
    fecha = serializers.DateField(source='horario.fecha')
    hora_inicio = serializers.TimeField(source='horario.hora_inicio', format='%H:%M')
    cupo_disponible = serializers.IntegerField()
