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
        
        def test_noti_publicacion(self):
            self.notificacion_1 = NotificacionPublicacion.objects.create(autor=self.perfil1, publicacion=self.publicacion, destinatario=self.perfil2)

        def test_noti_comentario(self):
            self.notificacio_2 = NotificacionComentario.objects.create(autor=self.perfil1, publicacion=self.publicacion, destinatario=self.publicacion.autor)

        def test_noti_seguir(self):
            self.notificacion_3 = NotificacionSeguir.objects.create(destinatario=self.perfil2, usuario=self.perfil1)

        def test_noti_respuesta_comentario(self):
            self.notificacion_4 = NotificacionRespuestaComentario.objects.create(publicacion=self.publicacion, destinatario=self.comentario.autor, usuario=self.perfil1, comentario=self.comentario)

        def test_noti_me_gusta(self):
            self.notificacion_5 = NotificacionMeGusta.objects.create(publicacion=self.publicacion, destinatario=self.publicacion.autor, usuario=self.perfil2)

        def test_noti_mensaje(self):
            self.notificacion_6 = NotificacionMensaje.objects.create(destinatario=self.perfil1, usuario=self.perfil2, conversacion=self.conversacion, mensaje=self.mensaje1)
