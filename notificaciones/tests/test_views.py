from django.test import TestCase
from mensajes.models import Conversacion, Mensaje
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from notificaciones.models import NotificacionComentario, NotificacionMeGusta, NotificacionMensaje, NotificacionPublicacion, NotificacionRespuestaComentario, NotificacionSeguir
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy



class NotificacionesViewsTest(TestCase):
        def setUp(self):
            self.usuario1 = User.objects.create_user(username='palillo', password='1234', email='pepe@gmai.com')
            self.usuario2 = User.objects.create_user(username='paqui', password='5678', email='paqui@gmai.com')
            self.perfil1 = PerfilUsuario.objects.create(usuario=self.usuario1)
            self.perfil2 = PerfilUsuario.objects.create(usuario=self.usuario2)
            self.publicacion = Publicacion.objects.create(titulo='hola', autor=self.perfil1,contenido='hello')
            self.comentario = Comentario.objects.create(autor=self.perfil1, publicacion=self.publicacion, texto='que')
            self.conversacion = Conversacion.objects.create(usuario1=self.perfil1, usuario2=self.perfil2)
            self.mensaje1 = Mensaje.objects.create(conversacion=self.conversacion, autor=self.perfil1, destinatario=self.perfil2, contenido='Hola')
            self.notificacion_comentario = NotificacionComentario.objects.create(autor=self.perfil1, publicacion=self.publicacion, destinatario=self.perfil2, leida=False)
            self.notificacion_publicacion = NotificacionPublicacion.objects.create(autor=self.perfil1, publicacion=self.publicacion, destinatario=self.perfil2, leida=False)
            self.notificacion_respuesta_comentario = NotificacionRespuestaComentario.objects.create(publicacion=self.publicacion, destinatario=self.comentario.autor, usuario=self.perfil2, comentario=self.comentario, leida=False )
            self.notificacion_seguir = NotificacionSeguir.objects.create(destinatario=self.perfil1, usuario=self.perfil2, leida=False)
            self.notificacion_me_gusta = NotificacionMeGusta.objects.create(publicacion=self.publicacion, destinatario=self.publicacion.autor, usuario=self.perfil2, leida=False)
            self.notificacion_mensajes = NotificacionMensaje.objects.create(destinatario=self.perfil1, usuario=self.perfil2, mensaje=self.mensaje1, conversacion=self.conversacion, leida=False)

        def test_list_notificaciones(self):
            self.client.login(username='palillo', password='1234')
            url = reverse_lazy('notificaciones:lista')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


        def test_marcar_leida_comentario(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('notificaciones:marcar_leida_comentario', kwargs={'pk': self.notificacion_comentario.pk})
            response = self.client.get(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Notificacion leida correctamente'}
            )

        def test_marcar_leida_publicacion(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('notificaciones:marcar_leida_publicacion', kwargs={'pk': self.notificacion_publicacion.pk})
            response = self.client.get(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Notificacion leida correctamente'}
            )


        def test_marcar_leida_respuesta_comentario(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('notificaciones:marcar_leida_respuesta_comentario', kwargs={'pk': self.notificacion_respuesta_comentario.pk})
            response = self.client.get(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Notificacion leida correctamente'}
            )


        def test_marcar_leida_seguir(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('notificaciones:marcar_leida_seguir', kwargs={'pk': self.notificacion_seguir.pk})
            response = self.client.get(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Notificacion leida correctamente'}
            )


        def test_marcar_leida_me_gusta(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('notificaciones:marcar_leida_me_gusta', kwargs={'pk': self.notificacion_me_gusta.pk})
            response = self.client.get(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Notificacion leida correctamente'}
            )


        def test_marcar_leida_mensaje(self):
            self.client.login(username='paqui', password='5678')
            url = reverse_lazy('notificaciones:marcar_leida_mensaje', kwargs={'pk': self.notificacion_mensajes.pk})
            response = self.client.get(
                url,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'success': True,
            'mensaje': 'Notificacion leida correctamente'}
            )
