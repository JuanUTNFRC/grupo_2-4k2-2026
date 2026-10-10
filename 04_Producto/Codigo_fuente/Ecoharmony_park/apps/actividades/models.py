from django.core.validators import MinValueValidator
from django.db import models


class Actividad(models.Model):
    """Actividad del parque (Tirolesa, Safari, etc.). La carga el administrador."""

    nombre = models.CharField(max_length=50, unique=True)
    cupo_por_horario = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )
    requiere_talle = models.BooleanField(default=False)
    terminos_condiciones = models.TextField()
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'actividad'
        verbose_name_plural = 'actividades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    """Turno de una actividad. Dura una hora, por eso no se guarda la hora de fin."""

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.PROTECT,
        related_name='horarios',
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()

    class Meta:
        verbose_name = 'horario'
        verbose_name_plural = 'horarios'
        ordering = ['fecha', 'hora_inicio']
        constraints = [
            models.UniqueConstraint(
                fields=['actividad', 'fecha', 'hora_inicio'],
                name='horario_unico_por_actividad',
            ),
        ]

    def __str__(self):
        return f'{self.actividad} - {self.fecha} {self.hora_inicio:%H:%M}'
