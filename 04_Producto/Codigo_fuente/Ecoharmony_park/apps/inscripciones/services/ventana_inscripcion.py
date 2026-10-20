"""RN2: período en el que un horario admite inscripciones."""

from datetime import timedelta

APERTURA = timedelta(hours=24)
CIERRE = timedelta(minutes=15)


def abrio(horario, ahora):
    """La inscripción abre 24 horas antes del inicio del horario."""
    return ahora >= horario.inicio - APERTURA


def cerro(horario, ahora):
    """La inscripción cierra 15 minutos antes del inicio del horario."""
    return ahora >= horario.inicio - CIERRE


def esta_abierta(horario, ahora):
    return abrio(horario, ahora) and not cerro(horario, ahora)
