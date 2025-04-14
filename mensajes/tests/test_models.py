from django.test import TestCase
from mensajes.models import Conversacion, Mensaje
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from notificaciones.models import NotificacionComentario, NotificacionMeGusta, NotificacionMensaje, NotificacionPublicacion, NotificacionRespuestaComentario, NotificacionSeguir
from django.contrib.auth.models import User

class MensajesModelsTest(TestCase):
    def setUp(self):
    #creamos un mensaje
        self.usuario1 = User.objects.create(username='palillo', password='1234', email='pepe@gmai.com')
        self.usuario2 = User.objects.create(username='paqui', password='5678', email='paqui@gmai.com')
        self.perfil1 = PerfilUsuario.objects.create(usuario=self.usuario1)
        self.perfil2 = PerfilUsuario.objects.create(usuario=self.usuario2)
        self.conversacion = Conversacion.objects.create(usuario1=self.perfil1, usuario2=self.perfil2)
    
    def test_crear_conversacion(self):
        self.assertTrue(self.conversacion)

    def test_crear_mensaje(self):
        self.mensaje = Mensaje.objects.create(conversacion=self.conversacion, autor=self.perfil1, destinatario=self.perfil2, contenido='Hola')