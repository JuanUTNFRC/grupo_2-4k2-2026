from apps.inscripciones.models import Inscripcion, Participante


class InscripcionRepository:
    def participantes_inscriptos(self, horario_id):
        return Participante.objects.filter(inscripcion__horario_id=horario_id).count()

    def dnis_inscriptos(self, horario_id):
        return set(
            Participante.objects
            .filter(inscripcion__horario_id=horario_id)
            .values_list('dni', flat=True)
        )

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
