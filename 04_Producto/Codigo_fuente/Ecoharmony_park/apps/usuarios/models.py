from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Usuario del sistema. El email es único porque es el destino del mail
    de confirmación de la inscripción (con el código QR)."""

    email = models.EmailField('correo electrónico', unique=True)

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
