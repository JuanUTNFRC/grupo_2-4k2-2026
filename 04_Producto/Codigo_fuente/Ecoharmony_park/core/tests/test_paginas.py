from django.test import TestCase

from apps.usuarios.models import Usuario


class PaginasTests(TestCase):
    def test_la_pagina_de_inscripcion_sin_sesion_redirige_al_login(self):
        respuesta = self.client.get('/')

        self.assertRedirects(respuesta, '/login/?next=/')

    def test_la_pagina_de_inscripcion_con_sesion_se_muestra(self):
        usuario = Usuario.objects.create_user(
            username='visitante', email='visitante@example.com', password='x',
        )
        self.client.force_login(usuario)

        respuesta = self.client.get('/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'inscripciones/inscripcion.html')

    def test_la_pagina_de_login_se_muestra(self):
        respuesta = self.client.get('/login/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'registration/login.html')
