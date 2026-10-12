from datetime import date

from django.test import SimpleTestCase

from apps.actividades.services.calendario_service import CalendarioParqueService


class EstaAbiertoTests(SimpleTestCase):
    def setUp(self):
        self.calendario = CalendarioParqueService()

    def test_un_martes_el_parque_esta_abierto(self):
        martes = date(2026, 10, 13)

        self.assertTrue(self.calendario.esta_abierto(martes))
