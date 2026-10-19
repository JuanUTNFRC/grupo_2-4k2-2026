from rest_framework import serializers

from apps.inscripciones.models import Inscripcion, Participante


class ParticipanteSerializer(serializers.Serializer):
    # Los mensajes dicen cómo corregir el dato: el front los muestra debajo de cada campo.
    nombre = serializers.CharField(
        max_length=100,
        error_messages={
            'required': 'Ingresá el nombre y apellido.',
            'blank': 'Ingresá el nombre y apellido.',
            'max_length': 'El nombre puede tener hasta 100 caracteres.',
        },
    )
    dni = serializers.RegexField(
        r'^\d{7,8}$',
        error_messages={
            'required': 'Ingresá el DNI.',
            'blank': 'Ingresá el DNI.',
            'invalid': 'El DNI tiene que tener 7 u 8 números, sin puntos.',
        },
    )
    edad = serializers.IntegerField(
        min_value=1,
        max_value=130,
        error_messages={
            'required': 'Ingresá la edad.',
            'invalid': 'Ingresá la edad en números.',
            'min_value': 'La edad tiene que ser mayor a 0.',
            'max_value': 'La edad tiene que ser 130 o menos.',
        },
    )
    # Si el talle es obligatorio depende de la actividad: lo valida el service.
    talle = serializers.ChoiceField(
        choices=Participante.Talle.choices,
        allow_blank=True,
        default='',
        error_messages={'invalid_choice': 'Elegí un talle de la lista.'},
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
