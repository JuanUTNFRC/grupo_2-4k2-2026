from datetime import time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.actividades.models import Actividad, Horario
from apps.actividades.services.calendario_service import CalendarioParqueService

# RN1: actividades, cupos y talle.
ACTIVIDADES = [
    {
        'nombre': 'Tirolesa',
        'cupo_por_horario': 10,
        'requiere_talle': True,
        'terminos_condiciones': (
            'Es obligatorio usar el arnés provisto por el parque y seguir las '
            'indicaciones del guía en todo momento.'
        ),
    },
    {
        'nombre': 'Safari',
        'cupo_por_horario': 20,
        'requiere_talle': False,
        'terminos_condiciones': (
            'Está prohibido descender del vehículo y alimentar a los animales.'
        ),
    },
    {
        'nombre': 'Palestra',
        'cupo_por_horario': 12,
        'requiere_talle': True,
        'terminos_condiciones': (
            'Es obligatorio usar el arnés provisto por el parque y escalar solo '
            'con la supervisión del guía.'
        ),
    },
    {
        'nombre': 'Jardinería',
        'cupo_por_horario': 15,
        'requiere_talle': False,
        'terminos_condiciones': (
            'Las herramientas se usan solo bajo la supervisión del guía y se '
            'devuelven al finalizar la actividad.'
        ),
    },
]

# RN2: un turno por hora, de 09:00 a 17:00.
HORAS_INICIO = [time(hora, 0) for hora in range(9, 18)]


class Command(BaseCommand):
    help = 'Carga el usuario de prueba, las actividades y sus horarios.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            default='visitante@example.com',
            help='Email del usuario de prueba, destino del mail de confirmación.',
        )
        parser.add_argument(
            '--password',
            default='visitante1234',
            help='Contraseña del usuario de prueba.',
        )
        parser.add_argument(
            '--dias',
            type=int,
            default=30,
            help='Cantidad de días, desde hoy, para los que se generan horarios.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self._crear_usuario(options['email'], options['password'])
        actividades = self._crear_actividades()
        cantidad_horarios = self._crear_horarios(actividades, options['dias'])

        self.stdout.write(self.style.SUCCESS(
            f'Usuario "visitante" ({options["email"]}), '
            f'{len(actividades)} actividades y '
            f'{cantidad_horarios} horarios nuevos.'
        ))

    def _crear_usuario(self, email, password):
        usuario, _ = get_user_model().objects.update_or_create(
            username='visitante',
            defaults={'email': email},
        )
        usuario.set_password(password)
        usuario.save()

    def _crear_actividades(self):
        actividades = []
        for datos in ACTIVIDADES:
            actividad, _ = Actividad.objects.update_or_create(
                nombre=datos['nombre'],
                defaults={**datos, 'activa': True},
            )
            actividades.append(actividad)
        return actividades

    def _crear_horarios(self, actividades, dias):
        calendario = CalendarioParqueService()
        hoy = timezone.localdate()
        creados = 0
        for desplazamiento in range(dias):
            fecha = hoy + timedelta(days=desplazamiento)
            for hora_inicio in HORAS_INICIO:
                if not calendario.admite_actividad(fecha, hora_inicio):
                    continue
                for actividad in actividades:
                    _, creado = Horario.objects.get_or_create(
                        actividad=actividad,
                        fecha=fecha,
                        hora_inicio=hora_inicio,
                    )
                    creados += creado
        return creados
