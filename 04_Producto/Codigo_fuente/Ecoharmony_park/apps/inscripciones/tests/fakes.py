"""Dobles de prueba en memoria para testear InscripcionService sin base de datos."""

from apps.inscripciones.models import Inscripcion


class FakeHorarioService:
    def __init__(self, horarios=()):
        self.horarios = {horario.id: horario for horario in horarios}

    def obtener(self, horario_id):
        return self.horarios.get(horario_id)


class FakeInscripcionRepository:
    def __init__(self):
        self.creadas = []

    def crear(self, usuario, horario, acepta_terminos, participantes):
        inscripcion = Inscripcion(
            usuario=usuario,
            horario=horario,
            acepta_terminos=acepta_terminos,
        )
        self.creadas.append({'inscripcion': inscripcion, 'participantes': participantes})
        return inscripcion


class NotificadorEspia:
    """Registra las inscripciones notificadas en lugar de enviar el mail."""

    def __init__(self):
        self.notificadas = []

    def notificar(self, inscripcion):
        self.notificadas.append(inscripcion)
