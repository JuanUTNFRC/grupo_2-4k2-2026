from apps.inscripciones.exceptions.inscripcion_exceptions import CupoInsuficienteError


class InscripcionService:
    """Reglas de negocio de la inscripción a una actividad.

    Recibe datos ya validados en formato por InscripcionCreateSerializer.
    """

    def __init__(self, inscripcion_repository, horario_service, notificador):
        self.inscripciones = inscripcion_repository
        self.horarios = horario_service
        self.notificador = notificador

    def inscribir(self, usuario, datos):
        horario = self.horarios.obtener(datos['horario_id'])
        ocupados = self.inscripciones.participantes_inscriptos(horario.id)
        disponibles = horario.actividad.cupo_por_horario - ocupados
        if len(datos['participantes']) > disponibles:
            raise CupoInsuficienteError('El horario no tiene cupo para todos los participantes.')

        inscripcion = self.inscripciones.crear(
            usuario=usuario,
            horario=horario,
            acepta_terminos=datos['acepta_terminos'],
            participantes=datos['participantes'],
        )
        self.notificador.notificar(inscripcion)
        return inscripcion
