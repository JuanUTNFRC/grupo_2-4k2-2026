from django.test import SimpleTestCase

from apps.inscripciones.serializers import InscripcionCreateSerializer


def datos_validos():
    return {
        'actividad_id': 1,
        'horario_id': 10,
        'acepta_terminos': True,
        'participantes': [
            {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': 'M'},
        ],
    }


class InscripcionCreateSerializerTests(SimpleTestCase):
    def test_una_solicitud_valida_es_valida(self):
        serializer = InscripcionCreateSerializer(data=datos_validos())

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data, datos_validos())

    def test_sin_participantes_es_invalida(self):
        datos = datos_validos()
        datos['participantes'] = []

        serializer = InscripcionCreateSerializer(data=datos)

        self.assertFalse(serializer.is_valid())
        self.assertIn('participantes', serializer.errors)
