class InscripcionError(Exception):
    """Base de los rechazos de inscripción por reglas de negocio."""


class CupoInsuficienteError(InscripcionError):
    """RN4: el horario no tiene cupo para todos los participantes."""
