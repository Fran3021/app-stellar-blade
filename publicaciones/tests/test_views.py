from django.test import TestCase
from mensajes.models import Conversacion, Mensaje
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from notificaciones.models import NotificacionComentario, NotificacionMeGusta, NotificacionMensaje, NotificacionPublicacion, NotificacionRespuestaComentario, NotificacionSeguir
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

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

        def test_crear_publicacion(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('publicaciones:crear')
            response = self.client.post(url,
                {'titulo': 'prueba',
                'contenido': 'contenido',
                }, follow=True)
            self.assertEqual(response.status_code, 200)
            self.publicacion = Publicacion.objects.first()
            self.assertIsNotNone(self.publicacion)
            self.assertEqual(Publicacion.objects.count(), 2)
            self.assertEqual(self.publicacion.titulo, 'prueba')
            self.assertEqual(self.publicacion.contenido, 'contenido')
            self.assertEqual(self.publicacion.autor, self.perfil2)

        
        def test_detalle_publicacion(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('publicaciones:detalle', kwargs={'pk': self.publicacion.pk})
            response = self.client.post(url,
                {'publicacion': self.publicacion,
                'texto': 'texto',
                'destinatario': self.publicacion.autor.pk,
                }, follow=True)
            self.assertEqual(response.status_code, 200)
            self.comentario = Comentario.objects.first()
            self.assertEqual(self.comentario.texto, 'texto')
            self.assertEqual(self.comentario.autor, self.perfil2)


        def test_editar_publicacion(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('publicaciones:editar', kwargs={'pk': self.publicacion.pk})
            response = self.client.post(url,
                {'titulo': 'prueba',
                'contenido': 'contenido',
                }, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.publicacion.titulo, 'prueba')
            self.assertEqual(self.publicacion.contenido, 'contenido')


        def test_eliminar_publicacion(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('publicaciones:delete', kwargs={'pk': self.publicacion.pk})
            response = self.client.delete(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Publicacion.objects.filter(titulo='prueba'))


        def test_contestar_comentario(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('publicaciones:contestar_comentario', kwargs={'pk': self.comentario.pk})
            response = self.client.post(
                url,
                {'respuesta':'respuesta',
                'publicacion_pk': self.publicacion.pk},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.respuesta = RespuestaComentario.objects.first()
            self.assertIsNotNone(self.respuesta)
            self.assertEqual(self.respuesta.respuesta, 'respuesta')


        def test_like(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('publicaciones:like', kwargs={'pk': self.publicacion.pk})
            response = self.client.get(url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertTrue(self.publicacion.likes.filter(pk=self.perfil1.pk).exists())


        def test_eliminar_comentario(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('publicaciones:eliminar_comentario', kwargs={'pk': self.comentario.pk})
            response = self.client.delete(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Se ha eliminado el comentario',}
            )


        def test_eliminar_respuesta_comentario(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('publicaciones:eliminar_respuesta', kwargs={'pk': self.respuesta_comentario.pk})
            response = self.client.delete(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Se ha eliminado la respuesta',}
            )

