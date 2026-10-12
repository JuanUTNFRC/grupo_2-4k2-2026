from apps.inscripciones.models import Inscripcion, Participante


class InscripcionRepository:
    def crear(self, usuario, horario, acepta_terminos, participantes):
        inscripcion = Inscripcion.objects.create(
            usuario=usuario,
            horario=horario,
            acepta_terminos=acepta_terminos,
        )
        Participante.objects.bulk_create(
            Participante(inscripcion=inscripcion, **datos) for datos in participantes
        )
        return inscripcion
