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


def con_participante(**cambios):
    """Datos válidos con el único participante modificado. `None` quita el campo."""
    datos = datos_validos()
    participante = datos['participantes'][0]
    for campo, valor in cambios.items():
        if valor is None:
            del participante[campo]
        else:
            participante[campo] = valor
    return datos


class ParticipanteSerializerTests(SimpleTestCase):
    def assertParticipanteInvalido(self, datos, campo):
        serializer = InscripcionCreateSerializer(data=datos)

        self.assertFalse(serializer.is_valid())
        self.assertIn(campo, serializer.errors['participantes'][0])

    def test_sin_nombre_es_invalido(self):
        self.assertParticipanteInvalido(con_participante(nombre=None), 'nombre')

    def test_nombre_en_blanco_es_invalido(self):
        self.assertParticipanteInvalido(con_participante(nombre='   '), 'nombre')

    def test_nombre_de_mas_de_100_caracteres_es_invalido(self):
        self.assertParticipanteInvalido(con_participante(nombre='a' * 101), 'nombre')
