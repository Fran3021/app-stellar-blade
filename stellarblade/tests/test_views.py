from django.test import TestCase
from mensajes.models import Conversacion, Mensaje
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from notificaciones.models import NotificacionComentario, NotificacionMeGusta, NotificacionMensaje, NotificacionPublicacion, NotificacionRespuestaComentario, NotificacionSeguir
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile

class StellarBladeViewsTest(TestCase):
        def setUp(self):
            self.usuario1 = User.objects.create_user(username='palillo', password='1234', email='pepe@gmai.com')
            self.usuario2 = User.objects.create_user(username='paqui', password='5678', email='paqui@gmai.com')
            self.perfil1 = PerfilUsuario.objects.create(usuario=self.usuario1)
            self.perfil2 = PerfilUsuario.objects.create(usuario=self.usuario2)
            self.publicacion = Publicacion.objects.create(titulo='prueba', autor=self.perfil2,contenido='contenido')
            self.comentario = Comentario.objects.create(autor=self.perfil2, publicacion=self.publicacion, texto='texto')
            self.conversacion = Conversacion.objects.create(usuario1=self.perfil1, usuario2=self.perfil2)
            self.mensaje1 = Mensaje.objects.create(conversacion=self.conversacion, autor=self.perfil1, destinatario=self.perfil2, contenido='Hola')
            self.respuesta_comentario = RespuestaComentario.objects.create(autor=self.perfil1, publicacion=self.publicacion, comentario=self.comentario, respuesta='respuesta')

        
        def test_home(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('home')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


        def test_legal(self):
            url = reverse_lazy('politica_legal')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        

        def test_logout(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('logout')
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)

        
        def test_registro(self):
            url = reverse_lazy('registro')
            response = self.client.post(url,
                {'username': 'kito',
                'email': 'k@k.com',
                'password': '1369',
                'password_confirm': '1369'}, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(User.objects.filter(username='kito'))
        
        def test_login(self):
            url = reverse_lazy('login')
            response = self.client.post(url,
                {'username': 'palillo',
                'password': '1234'}, follow=True)
            self.assertEqual(response.status_code, 200)
        

        def test_search(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('search')
            response = self.client.get(url, 
            {
                'value': 'prueba',
            },follow=True)
            self.assertEqual(response.status_code, 200)

        
        def test_info_juego(self):
            url = reverse_lazy('info_del_juego')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


        def test_politica_legal(self):
            url = reverse_lazy('politica_legal')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)