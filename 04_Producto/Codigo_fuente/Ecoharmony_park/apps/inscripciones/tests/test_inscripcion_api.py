from datetime import time, timedelta

from django.core import mail
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.usuarios.models import Usuario

URL = '/api/inscripciones/'


def proximo_martes():
    hoy = timezone.localdate()
    return hoy + timedelta(days=(1 - hoy.weekday()) % 7 or 7)


def participante(**cambios):
    return {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': '', **cambios}


class InscripcionApiTests(APITestCase):
    """Pruebas de usuario PU1 a PU6 de punta a punta por HTTP."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        self.client.force_authenticate(self.usuario)
        self.tirolesa = Actividad.objects.create(
            nombre='Tirolesa', cupo_por_horario=10, requiere_talle=True,
            terminos_condiciones='T&C',
        )
        self.horario_tirolesa = Horario.objects.create(
            actividad=self.tirolesa, fecha=proximo_martes(), hora_inicio=time(10, 0),
        )

    def solicitud(self, actividad, horario, **cambios):
        return {
            'actividad_id': actividad.id,
            'horario_id': horario.id,
            'acepta_terminos': True,
            'participantes': [participante(talle='M')],
            **cambios,
        }

    def test_pu1_inscripcion_valida_con_talle_responde_201_y_envia_el_mail(self):
        respuesta = self.client.post(
            URL, self.solicitud(self.tirolesa, self.horario_tirolesa), format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(respuesta.data['actividad'], 'Tirolesa')
        self.assertEqual(respuesta.data['participantes'], [participante(talle='M')])
        self.assertEqual(len(mail.outbox), 1)

    def test_pu2_horario_sin_cupo_responde_409(self):
        InscripcionRepository().crear(
            usuario=self.usuario,
            horario=self.horario_tirolesa,
            acepta_terminos=True,
            participantes=[
                participante(dni=f'3000000{n}', talle='M')
                for n in range(self.tirolesa.cupo_por_horario)
            ],
        )

        respuesta = self.client.post(
            URL, self.solicitud(self.tirolesa, self.horario_tirolesa), format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(respuesta.data, {
            'codigo': 'cupo_insuficiente',
            'detalle': 'El horario no tiene cupo para todos los participantes.',
        })

    def test_pu3_sin_talle_en_una_actividad_que_no_lo_requiere_responde_201(self):
        safari = Actividad.objects.create(
            nombre='Safari', cupo_por_horario=20, terminos_condiciones='T&C',
        )
        horario = Horario.objects.create(
            actividad=safari, fecha=proximo_martes(), hora_inicio=time(10, 0),
        )

        respuesta = self.client.post(
            URL, self.solicitud(safari, horario, participantes=[participante()]), format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)

    def test_pu4_horario_con_el_parque_cerrado_responde_400(self):
        lunes = proximo_martes() + timedelta(days=6)
        horario_lunes = Horario.objects.create(
            actividad=self.tirolesa, fecha=lunes, hora_inicio=time(10, 0),
        )

        respuesta = self.client.post(
            URL, self.solicitud(self.tirolesa, horario_lunes), format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respuesta.data['codigo'], 'parque_cerrado')

    def test_pu5_sin_aceptar_los_terminos_responde_400(self):
        respuesta = self.client.post(
            URL,
            self.solicitud(self.tirolesa, self.horario_tirolesa, acepta_terminos=False),
            format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respuesta.data['codigo'], 'terminos_no_aceptados')

    def test_pu6_sin_talle_en_una_actividad_que_lo_requiere_responde_400(self):
        respuesta = self.client.post(
            URL,
            self.solicitud(self.tirolesa, self.horario_tirolesa, participantes=[participante()]),
            format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respuesta.data['codigo'], 'talle_requerido')

    def test_sin_autenticar_responde_403(self):
        self.client.force_authenticate(None)

        respuesta = self.client.post(
            URL, self.solicitud(self.tirolesa, self.horario_tirolesa), format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(respuesta.data['codigo'], 'not_authenticated')
        self.assertEqual(len(mail.outbox), 0)

    def test_datos_con_formato_invalido_responden_400_con_los_errores_por_campo(self):
        respuesta = self.client.post(
            URL,
            self.solicitud(self.tirolesa, self.horario_tirolesa, participantes=[participante(dni='abc')]),
            format='json',
        )

        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respuesta.data['codigo'], 'datos_invalidos')
        self.assertIn('dni', respuesta.data['errores']['participantes'][0])
