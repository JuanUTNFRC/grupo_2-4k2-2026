from django.test import SimpleTestCase

from apps.inscripciones.models import Inscripcion
from apps.inscripciones.notificaciones.cola_notificador import ColaNotificador


class TareaEspia:
    """Registra lo que se encola en lugar de mandarlo a Redis."""

    def __init__(self):
        self.encoladas = []

    def delay(self, *args):
        self.encoladas.append(args)


class ColaNotificadorTests(SimpleTestCase):
    def test_encola_el_envio_del_mail_con_el_id_de_la_inscripcion(self):
        tarea = TareaEspia()

        ColaNotificador(tarea=tarea).notificar(Inscripcion(id=7))

        self.assertEqual(tarea.encoladas, [(7,)])
