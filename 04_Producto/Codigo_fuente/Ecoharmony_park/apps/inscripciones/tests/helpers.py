"""Datos de prueba compartidos por los tests de inscripciones."""

from datetime import date, datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

# Un martes: el parque abre. AHORA es antes de todos sus turnos.
MARTES = date(2026, 10, 13)
AHORA = datetime(2026, 10, 13, 8, 0, tzinfo=ZoneInfo('America/Argentina/Cordoba'))


def participante(**cambios):
    """Datos válidos de un participante, en la forma de validated_data."""
    return {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': '', **cambios}


def fijar_reloj(test, ahora=AHORA):
    """Fija timezone.now() durante el test, para no depender del día en que se corre."""
    reloj = patch('django.utils.timezone.now', return_value=ahora)
    reloj.start()
    test.addCleanup(reloj.stop)
