from datetime import date

from django.test import SimpleTestCase

from apps.actividades.services.calendario_service import CalendarioParqueService


class EstaAbiertoTests(SimpleTestCase):
    def setUp(self):
        self.calendario = CalendarioParqueService()

    def test_un_martes_el_parque_esta_abierto(self):
        martes = date(2026, 10, 13)

        self.assertTrue(self.calendario.esta_abierto(martes))

    def test_un_lunes_el_parque_esta_cerrado(self):
        lunes = date(2026, 10, 12)

        self.assertFalse(self.calendario.esta_abierto(lunes))

    def test_el_1_de_enero_el_parque_esta_cerrado(self):
        anio_nuevo_viernes = date(2027, 1, 1)

        self.assertFalse(self.calendario.esta_abierto(anio_nuevo_viernes))

    def test_el_25_de_diciembre_el_parque_esta_cerrado(self):
        navidad_viernes = date(2026, 12, 25)

        self.assertFalse(self.calendario.esta_abierto(navidad_viernes))
