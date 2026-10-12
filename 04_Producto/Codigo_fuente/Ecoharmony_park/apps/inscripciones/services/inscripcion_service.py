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
        inscripcion = self.inscripciones.crear(
            usuario=usuario,
            horario=horario,
            acepta_terminos=datos['acepta_terminos'],
            participantes=datos['participantes'],
        )
        self.notificador.notificar(inscripcion)
        return inscripcion
