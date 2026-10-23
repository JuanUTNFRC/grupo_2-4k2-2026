from django.contrib import admin

from apps.inscripciones.models import Inscripcion, Participante


class ParticipanteInline(admin.TabularInline):
    model = Participante
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    """Solo lectura: las inscripciones se generan desde la app, no desde el admin."""

    list_display = ('codigo', 'usuario', 'horario', 'creada_en')
    list_filter = ('horario__actividad', 'horario__fecha')
    search_fields = ('usuario__email', 'participantes__dni')
    inlines = [ParticipanteInline]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
