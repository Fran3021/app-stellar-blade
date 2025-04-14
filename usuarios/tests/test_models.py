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
            self.notificacion_comentario = NotificacionComentario.objects.create(autor=self.perfil1, publicacion=self.publicacion, destinatario=self.perfil2, leida=False)
            self.notificacion_publicacion = NotificacionPublicacion.objects.create(autor=self.perfil1, publicacion=self.publicacion, destinatario=self.perfil2, leida=False)
            self.notificacion_respuesta_comentario = NotificacionRespuestaComentario.objects.create(publicacion=self.publicacion, destinatario=self.comentario.autor, usuario=self.perfil2, comentario=self.comentario, leida=False )
            self.notificacion_seguir = NotificacionSeguir.objects.create(destinatario=self.perfil2, usuario=self.perfil2, leida=False)
            self.notificacion_me_gusta = NotificacionMeGusta.objects.create(publicacion=self.publicacion, destinatario=self.publicacion.autor, usuario=self.perfil2, leida=False)
            self.notificacion_mensajes = NotificacionMensaje.objects.create(destinatario=self.perfil1, usuario=self.perfil2, mensaje=self.mensaje1, conversacion=self.conversacion, leida=False)
        

        def test_crear_usuario(self):
            self.usuario = User.objects.create_user(username='lilia', password='2468', email='h@h.com')
            self.perfil = PerfilUsuario.objects.create(usuario=self.usuario)
        

        def test_follow(self):
            self.perfil1.follow(perfil=self.perfil2)
            self.assertTrue(Follow.objects.filter(seguidor=self.perfil1, siguiendo=self.perfil2))
        

        def test_unfollow(self):
            self.perfil1.follow(perfil=self.perfil2)
            self.perfil1.unfollow(perfil=self.perfil2)
            self.assertFalse(Follow.objects.filter(seguidor=self.perfil1, siguiendo=self.perfil2))

        
        def test_like_pub(self):
            self.perfil1.like_pub(self.publicacion)
            self.assertTrue(self.publicacion.likes.filter(pk=self.perfil1.pk).exists())

        
        def test_unlike_pub(self):
            self.perfil1.like_pub(self.publicacion)
            self.perfil1.unlike_pub(self.publicacion)
            self.assertFalse(self.publicacion.likes.filter(pk=self.perfil1.pk).exists())

        
        def test_total_publicaciones(self):
            self.total = self.perfil1.total_notificaciones()
            #ponemos 1 porque solo he configurado que tenga una notificacion arrivba en el setUp
            self.assertEqual(self.total, 1)