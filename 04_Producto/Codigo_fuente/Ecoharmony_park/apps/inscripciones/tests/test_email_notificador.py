from datetime import date, time
from smtplib import SMTPException
from unittest.mock import patch

from django.core import mail
from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.inscripciones.notificaciones.email_notificador import EmailNotificador
from apps.inscripciones.repositories.inscripcion_repository import InscripcionRepository
from apps.usuarios.models import Usuario


class EmailNotificadorTests(TestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        tirolesa = Actividad.objects.create(
            nombre='Tirolesa', cupo_por_horario=10, requiere_talle=True,
            terminos_condiciones='T&C',
        )
        horario = Horario.objects.create(
            actividad=tirolesa, fecha=date(2026, 10, 13), hora_inicio=time(10, 0),
        )
        self.inscripcion = InscripcionRepository().crear(
            usuario=usuario,
            horario=horario,
            acepta_terminos=True,
            participantes=[
                {'nombre': 'Ana Pérez', 'dni': '30123456', 'edad': 30, 'talle': 'M'},
                {'nombre': 'Juan Gómez', 'dni': '1234567', 'edad': 8, 'talle': 'XS'},
            ],
        )

    def test_envia_un_mail_al_usuario_con_actividad_fecha_y_hora_en_el_asunto(self):
        EmailNotificador().notificar(self.inscripcion)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['visitante@example.com'])
        self.assertEqual(
            mail.outbox[0].subject, 'Inscripción confirmada: Tirolesa - 13/10/2026 10:00',
        )

    def test_el_cuerpo_texto_y_html_tienen_los_datos_de_la_inscripcion(self):
        EmailNotificador().notificar(self.inscripcion)

        mensaje = mail.outbox[0]
        html = [contenido for contenido, tipo in mensaje.alternatives if tipo == 'text/html']
        self.assertEqual(len(html), 1)
        esperado = [
            str(self.inscripcion.codigo), 'Tirolesa', '13/10/2026', '10:00',
            'Ana Pérez', '30123456', 'Talle M', 'Juan Gómez', '1234567', 'Talle XS',
        ]
        for formato, cuerpo in [('texto', mensaje.body), ('html', html[0])]:
            for dato in esperado:
                with self.subTest(formato=formato, dato=dato):
                    self.assertIn(dato, cuerpo)

    def test_el_codigo_qr_va_embebido_en_el_html_del_mail(self):
        EmailNotificador().notificar(self.inscripcion)

        mensaje = mail.outbox[0]
        imagenes = [
            parte for parte in mensaje.message().walk()
            if parte.get_content_type() == 'image/png'
        ]
        self.assertEqual(len(imagenes), 1)
        qr = imagenes[0]
        self.assertEqual(qr['Content-ID'], '<qr-inscripcion>')
        self.assertEqual(qr.get_content_disposition(), 'inline')
        self.assertEqual(qr.get_filename(), f'inscripcion_{self.inscripcion.codigo}.png')
        self.assertTrue(qr.get_content().startswith(b'\x89PNG\r\n\x1a\n'))
        html = next(contenido for contenido, tipo in mensaje.alternatives if tipo == 'text/html')
        self.assertIn('src="cid:qr-inscripcion"', html)

    def test_si_falla_el_envio_registra_el_error_sin_propagarlo(self):
        with (
            patch('django.core.mail.EmailMultiAlternatives.send', side_effect=SMTPException('caído')),
            self.assertLogs('apps.inscripciones.notificaciones', level='ERROR') as logs,
        ):
            EmailNotificador().notificar(self.inscripcion)

        self.assertIn(str(self.inscripcion.codigo), logs.output[0])
