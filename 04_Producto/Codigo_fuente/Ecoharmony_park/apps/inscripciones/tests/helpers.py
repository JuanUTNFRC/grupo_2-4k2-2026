"""Datos de prueba compartidos por los tests de inscripciones."""

from datetime import timedelta

from django.utils import timezone


def participante(**cambios):
    """Datos válidos de un participante, en la forma de validated_data."""
    return {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': '', **cambios}


def proximo_martes():
    """Un martes futuro: el parque abre y ningún horario del día comenzó."""
    hoy = timezone.localdate()
    return hoy + timedelta(days=(1 - hoy.weekday()) % 7 or 7)
