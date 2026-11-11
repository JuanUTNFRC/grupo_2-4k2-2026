from django.test import SimpleTestCase
from rest_framework.exceptions import APIException, Throttled

from core.exception_handler import exception_handler


class ExceptionHandlerTests(SimpleTestCase):
    def test_una_excepcion_que_drf_no_maneja_se_deja_pasar(self):
        # Sin respuesta, Django la convierte en un 500 y queda en el log.
        self.assertIsNone(exception_handler(ValueError('bug'), context={}))

    def test_una_excepcion_de_drf_sale_con_el_formato_uniforme(self):
        respuesta = exception_handler(Throttled(wait=30), context={})

        self.assertEqual(respuesta.status_code, 429)
        self.assertEqual(respuesta.data['codigo'], 'throttled')
        self.assertIn('detalle', respuesta.data)

    def test_un_detalle_con_forma_desconocida_se_deja_como_esta(self):
        respuesta = exception_handler(APIException({'campo': 'mal'}), context={})

        self.assertEqual(respuesta.data, {'campo': 'mal'})
