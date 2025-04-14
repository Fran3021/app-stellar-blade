from django.test import TestCase
from mensajes.models import Conversacion, Mensaje
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from notificaciones.models import NotificacionComentario, NotificacionMeGusta, NotificacionMensaje, NotificacionPublicacion, NotificacionRespuestaComentario, NotificacionSeguir
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

class PublicacionesModelsTest(TestCase):
        def setUp(self):
            self.usuario1 = User.objects.create_user(username='palillo', password='1234', email='pepe@gmai.com')
            self.usuario2 = User.objects.create_user(username='paqui', password='5678', email='paqui@gmai.com')
            self.perfil1 = PerfilUsuario.objects.create(usuario=self.usuario1)
            self.perfil2 = PerfilUsuario.objects.create(usuario=self.usuario2)
            self.publicacion = Publicacion.objects.create(titulo='hola', autor=self.perfil1,contenido='hello')
            self.comentario = Comentario.objects.create(autor=self.perfil1, publicacion=self.publicacion, texto='que')
            self.conversacion = Conversacion.objects.create(usuario1=self.perfil1, usuario2=self.perfil2)
            self.mensaje1 = Mensaje.objects.create(conversacion=self.conversacion, autor=self.perfil1, destinatario=self.perfil2, contenido='Hola')

        def test_crear_publicacion(self):
            self.publicacion = Publicacion.objects.create(titulo='what', autor = self.perfil1, contenido='the')

        def test_likes(self):
            self.publicacion.like(self.perfil1)
            self.assertTrue(self.publicacion.likes.filter(pk=self.perfil1.pk).exists())

        def test_unlikes(self):
            self.publicacion.like(self.perfil1)
            self.publicacion.unlike(self.perfil1)
            self.assertFalse(self.publicacion.likes.filter(pk=self.perfil1.pk).exists())

        def test_crear_comentario(self):
            self.comentario = Comentario.objects.create(autor=self.perfil1, publicacion=self.publicacion, texto='hello')

        def test_respuesta_comentario(self):
            self.respuesta_comentario = RespuestaComentario.objects.create(autor=self.comentario.autor, publicacion=self.publicacion, comentario=self.comentario, respuesta='bye')