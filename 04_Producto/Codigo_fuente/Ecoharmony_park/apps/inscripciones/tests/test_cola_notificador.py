from django.test import SimpleTestCase

from apps.inscripciones.models import Inscripcion
from apps.inscripciones.notificaciones.cola_notificador import ColaNotificador


class TareaEspia:
    """Registra lo que se encola en lugar de mandarlo a Redis."""

    def __init__(self):
        self.encoladas = []

    def delay(self, *args):
        self.encoladas.append(args)


class TareaSinBroker:
    """Simula que Redis no responde al encolar."""

    def delay(self, *args):
        raise ConnectionError('Redis no responde')


class ColaNotificadorTests(SimpleTestCase):
    def test_encola_el_envio_del_mail_con_el_id_de_la_inscripcion(self):
        tarea = TareaEspia()

        ColaNotificador(tarea=tarea).notificar(Inscripcion(id=7))

        self.assertEqual(tarea.encoladas, [(7,)])

    def test_si_no_puede_encolar_registra_el_error_sin_propagarlo(self):
        with self.assertLogs('apps.inscripciones.notificaciones', level='ERROR') as logs:
            ColaNotificador(tarea=TareaSinBroker()).notificar(Inscripcion(id=7))

        self.assertIn('7', logs.output[0])
