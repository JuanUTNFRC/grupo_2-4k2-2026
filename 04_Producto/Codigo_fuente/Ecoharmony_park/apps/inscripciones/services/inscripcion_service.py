from apps.inscripciones.exceptions.inscripcion_exceptions import (
    CupoInsuficienteError,
    ParqueCerradoError,
    TalleRequeridoError,
    TerminosNoAceptadosError,
)


class InscripcionService:
    """Reglas de negocio de la inscripción a una actividad.

    Recibe datos ya validados en formato por InscripcionCreateSerializer.
    """

    def __init__(self, inscripcion_repository, horario_service, notificador, calendario):
        self.inscripciones = inscripcion_repository
        self.horarios = horario_service
        self.notificador = notificador
        self.calendario = calendario

    def inscribir(self, usuario, datos):
        horario = self.horarios.obtener(datos['horario_id'])
        if not self.calendario.admite_actividad(horario.fecha, horario.hora_inicio):
            raise ParqueCerradoError()
        if not datos['acepta_terminos']:
            raise TerminosNoAceptadosError()
        self._validar_talles(horario.actividad, datos['participantes'])

        # El cupo se valida y se ocupa con el horario bloqueado, para que dos
        # inscripciones simultáneas no tomen el mismo lugar.
        with self.inscripciones.bloquear_horario(horario.id):
            self._validar_cupo(horario, datos['participantes'])
            inscripcion = self.inscripciones.crear(
                usuario=usuario,
                horario=horario,
                acepta_terminos=datos['acepta_terminos'],
                participantes=datos['participantes'],
            )

        self.notificador.notificar(inscripcion)
        return inscripcion

    def _validar_talles(self, actividad, participantes):
        if actividad.requiere_talle and any(not p['talle'] for p in participantes):
            raise TalleRequeridoError()

    def _validar_cupo(self, horario, participantes):
        ocupados = self.inscripciones.participantes_inscriptos(horario.id)
        disponibles = horario.actividad.cupo_por_horario - ocupados
        if len(participantes) > disponibles:
            raise CupoInsuficienteError()
