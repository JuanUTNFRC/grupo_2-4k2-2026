from rest_framework import status
from rest_framework.exceptions import APIException


class InscripcionError(APIException):
    """Base de los rechazos de inscripción por reglas de negocio."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'No se pudo realizar la inscripción.'
    default_code = 'inscripcion_invalida'


class CupoInsuficienteError(InscripcionError):
    """RN4: el horario no tiene cupo para todos los participantes."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = 'El horario no tiene cupo para todos los participantes.'
    default_code = 'cupo_insuficiente'


class TalleRequeridoError(InscripcionError):
    """RN1 y RN5: la actividad requiere talle y algún participante no lo indicó."""

    default_detail = 'La actividad requiere indicar el talle de cada participante.'
    default_code = 'talle_requerido'
