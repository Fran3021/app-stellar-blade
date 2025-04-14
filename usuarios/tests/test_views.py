from django.test import TestCase
from mensajes.models import Conversacion, Mensaje
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from notificaciones.models import NotificacionComentario, NotificacionMeGusta, NotificacionMensaje, NotificacionPublicacion, NotificacionRespuestaComentario, NotificacionSeguir
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile

class PublicacionesViewsTest(TestCase):
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

        
        def test_mi_perfil_view(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('usuarios:mi_perfil', kwargs={'pk': self.perfil1.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


        def test_editar_perfil(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('usuarios:update', kwargs={'pk': self.perfil2.pk})
            response = self.client.post(url,
                {'biografia': 'hola',
                'fecha_nacimiento': '30/09/1990',
                }, follow=True)
            self.perfil2.refresh_from_db()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.perfil2.biografia, 'hola')
            self.assertEqual(str(self.perfil2.fecha_nacimiento), '1990-09-30')



        def test_publicaciones_mis_contactos(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('usuarios:mis_contactos')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


        def test_follow(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('usuarios:follow', kwargs={'pk': self.perfil2.pk})
            response = self.client.get(url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertTrue(self.perfil2.siguiendo.filter(pk=self.perfil1.pk).exists())


        def test_perfiles_detalles(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('usuarios:detail', kwargs={'pk': self.perfil1.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)



