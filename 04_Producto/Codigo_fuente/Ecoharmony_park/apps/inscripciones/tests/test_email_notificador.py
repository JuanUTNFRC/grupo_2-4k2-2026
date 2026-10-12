from datetime import date, time

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

    def test_adjunta_el_codigo_qr_de_la_inscripcion_como_png(self):
        EmailNotificador().notificar(self.inscripcion)

        adjuntos = mail.outbox[0].attachments
        self.assertEqual(len(adjuntos), 1)
        nombre, contenido, tipo = adjuntos[0]
        self.assertEqual(nombre, f'inscripcion_{self.inscripcion.codigo}.png')
        self.assertEqual(tipo, 'image/png')
        self.assertTrue(contenido.startswith(b'\x89PNG\r\n\x1a\n'))
