from contextlib import contextmanager

from django.db import transaction
from django.db.models import Count

from apps.actividades.models import Horario
from apps.inscripciones.models import Inscripcion, Participante


class InscripcionRepository:
    @contextmanager
    def bloquear_horario(self, horario_id):
        """Transacción con la fila del horario bloqueada hasta el commit o rollback.

        En motores sin select_for_update (SQLite) Django omite el bloqueo.
        """
        with transaction.atomic():
            Horario.objects.select_for_update().get(id=horario_id)
            yield

    def obtener(self, inscripcion_id):
        """Inscripción con su usuario, horario y actividad cargados."""
        return (
            Inscripcion.objects
            .select_related('usuario', 'horario__actividad')
            .get(id=inscripcion_id)
        )

    def participantes_inscriptos(self, horario_id):
        return self._participantes_del_horario(horario_id).count()

    def participantes_por_horario(self, horario_ids):
        """Participantes inscriptos por horario, con 0 para los horarios sin inscriptos."""
        conteos = (
            Participante.objects
            .filter(inscripcion__horario_id__in=horario_ids)
            .values('inscripcion__horario_id')
            .annotate(total=Count('id'))
        )
        ocupados = {horario_id: 0 for horario_id in horario_ids}
        ocupados.update({c['inscripcion__horario_id']: c['total'] for c in conteos})
        return ocupados

    def dnis_inscriptos(self, horario_id):
        return set(self._participantes_del_horario(horario_id).values_list('dni', flat=True))

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

    def _participantes_del_horario(self, horario_id):
        return Participante.objects.filter(inscripcion__horario_id=horario_id)
