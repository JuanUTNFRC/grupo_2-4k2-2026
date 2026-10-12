from django.contrib import admin

from apps.actividades.models import Actividad, Horario


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cupo_por_horario', 'requiere_talle', 'activa')
    list_filter = ('activa', 'requiere_talle')
    search_fields = ('nombre',)


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'fecha', 'hora_inicio')
    list_filter = ('actividad', 'fecha')
    date_hierarchy = 'fecha'
