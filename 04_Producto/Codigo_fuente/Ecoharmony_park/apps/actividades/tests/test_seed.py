from io import StringIO

from django.contrib.auth import authenticate
from django.core.management import call_command
from django.test import TestCase

from apps.actividades.models import Actividad, Horario
from apps.actividades.services.calendario_service import CalendarioParqueService


def correr_seed(**opciones):
    salida = StringIO()
    call_command('seed', dias=8, stdout=salida, **opciones)
    return salida.getvalue()


class SeedTests(TestCase):
    def test_crea_las_cuatro_actividades_de_rn1(self):
        correr_seed()

        self.assertEqual(
            list(Actividad.objects.order_by('nombre').values_list('nombre', 'cupo_por_horario', 'requiere_talle')),
            [('Jardinería', 15, False), ('Palestra', 12, True), ('Safari', 20, False), ('Tirolesa', 10, True)],
        )

    def test_crea_el_usuario_de_prueba_con_el_email_indicado(self):
        correr_seed(email='prueba@example.com', password='clave-de-prueba')

        usuario = authenticate(username='visitante', password='clave-de-prueba')
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.email, 'prueba@example.com')

    def test_solo_crea_horarios_que_el_parque_admite(self):
        correr_seed()

        calendario = CalendarioParqueService()
        horarios = Horario.objects.all()
        self.assertTrue(horarios.exists())
        for horario in horarios:
            with self.subTest(horario=str(horario)):
                self.assertTrue(calendario.admite_actividad(horario.fecha, horario.hora_inicio))

    def test_correrlo_dos_veces_no_duplica_datos(self):
        correr_seed()
        horarios = Horario.objects.count()

        salida = correr_seed()

        self.assertEqual(Actividad.objects.count(), 4)
        self.assertEqual(Horario.objects.count(), horarios)
        self.assertIn('0 horarios nuevos', salida)
