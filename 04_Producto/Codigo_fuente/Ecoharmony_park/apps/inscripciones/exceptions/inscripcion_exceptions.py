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


class EdadMinimaError(InscripcionError):
    """RN5: algún participante no tiene la edad mínima de la actividad."""

    default_detail = 'Algún participante no tiene la edad mínima de la actividad.'
    default_code = 'edad_minima'

    def __init__(self, edad_minima):
        super().__init__(f'La actividad requiere tener {edad_minima} años o más.')


class TerminosNoAceptadosError(InscripcionError):
    """RN6: no se aceptaron los términos y condiciones de la actividad."""

    default_detail = 'Debe aceptar los términos y condiciones de la actividad.'
    default_code = 'terminos_no_aceptados'


class ParqueCerradoError(InscripcionError):
    """RN3: el parque está cerrado en el día u horario de la actividad."""

    default_detail = 'El parque está cerrado en el horario seleccionado.'
    default_code = 'parque_cerrado'


class HorarioNoDisponibleError(InscripcionError):
    """RN1 y RN2: el horario no existe, es de otra actividad o la actividad está inactiva."""

    default_detail = 'El horario seleccionado no está disponible.'
    default_code = 'horario_no_disponible'


class InscripcionNoHabilitadaError(InscripcionError):
    """RN2: la inscripción a un horario abre 24 horas antes de su inicio."""

    default_detail = 'La inscripción a un horario abre 24 horas antes de su inicio.'
    default_code = 'inscripcion_no_habilitada'


class InscripcionCerradaError(InscripcionError):
    """RN2: la inscripción a un horario cierra 15 minutos antes de su inicio."""

    default_detail = 'La inscripción a un horario cierra 15 minutos antes de su inicio.'
    default_code = 'inscripcion_cerrada'


class DniDuplicadoError(InscripcionError):
    """RN5: un mismo DNI no puede inscribirse dos veces en el mismo horario."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Un mismo DNI no puede inscribirse dos veces en el mismo horario.'
    default_code = 'dni_duplicado'
