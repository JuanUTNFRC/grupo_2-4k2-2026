import uuid

from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.db import models


class Inscripcion(models.Model):
    """Inscripción de un usuario a un horario de una actividad."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='inscripciones',
    )
    horario = models.ForeignKey(
        'actividades.Horario',
        on_delete=models.PROTECT,
        related_name='inscripciones',
    )
    # Se guarda como evidencia del consentimiento de los términos y condiciones.
    acepta_terminos = models.BooleanField(default=False)
    # Identificador no adivinable que se codifica en el QR.
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'inscripción'
        verbose_name_plural = 'inscripciones'
        ordering = ['-creada_en']

    def __str__(self):
        return f'{self.usuario} - {self.horario}'


class Participante(models.Model):
    """Persona que participa de una inscripción. Es una foto de sus datos
    al momento de inscribirse, no una persona reutilizable."""

    class Talle(models.TextChoices):
        XS = 'XS', 'XS'
        S = 'S', 'S'
        M = 'M', 'M'
        L = 'L', 'L'
        XL = 'XL', 'XL'
        XXL = 'XXL', 'XXL'

    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='participantes',
    )
    nombre = models.CharField(max_length=100)
    dni = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'^\d{7,8}$', 'El DNI debe tener 7 u 8 dígitos.'),
        ],
    )
    edad = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(130)])
    # Vacío cuando la actividad no requiere talle.
    talle = models.CharField(max_length=3, choices=Talle.choices, blank=True)

    class Meta:
        verbose_name = 'participante'
        verbose_name_plural = 'participantes'

    def __str__(self):
        return f'{self.nombre} ({self.dni})'
