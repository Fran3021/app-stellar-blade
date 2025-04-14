from django.test import TestCase
from mensajes.models import Conversacion, Mensaje
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from notificaciones.models import NotificacionComentario, NotificacionMeGusta, NotificacionMensaje, NotificacionPublicacion, NotificacionRespuestaComentario, NotificacionSeguir
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

class MensajesViewsTest(TestCase):
        def setUp(self):
            self.usuario1 = User.objects.create_user(username='palillo', password='1234', email='pepe@gmai.com')
            self.usuario2 = User.objects.create_user(username='paqui', password='5678', email='paqui@gmai.com')
            self.perfil1 = PerfilUsuario.objects.create(usuario=self.usuario1)
            self.perfil2 = PerfilUsuario.objects.create(usuario=self.usuario2)
            self.conversacion = Conversacion.objects.create(usuario1=self.perfil1, usuario2=self.perfil2)
            self.mensaje1 = Mensaje.objects.create(conversacion=self.conversacion, autor=self.perfil1, destinatario=self.perfil2, contenido='Hola')
            self.mensaje2 = Mensaje.objects.create(conversacion=self.conversacion, autor=self.perfil2, destinatario=self.perfil1, contenido='Hello')
            self.notificacion_mensaje = NotificacionMensaje.objects.create(destinatario=self.perfil2, usuario=self.perfil1, mensaje=self.mensaje1, conversacion=self.conversacion)
        
        def test_create_mensaje_view(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('mensajes:nuevo', kwargs={'pk': self.perfil2.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_conversaciones_views(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('mensajes:conversaciones')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_conversaciones_details_views(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('mensajes:conversaciones_detail', kwargs={'pk': self.conversacion.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_contestar_mensaje(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('mensajes:contestar_mensaje', kwargs={'pk': self.mensaje1.pk})
            response = self.client.post(
                url,
                {'contenido': self.mensaje2},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True}
            )

        def test_eliminar_mensaje(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('mensajes:eliminar_mensaje', kwargs={'pk': self.mensaje1.pk})
            response = self.client.delete(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'message': 'Mensaje eliminado corectamente',}
            )

        def test_eliminar_conversacion(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('mensajes:eliminar_conversacion', kwargs={'pk': self.conversacion.pk})
            response = self.client.delete(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'message': 'Conversacion eliminida correctamente',}
            )