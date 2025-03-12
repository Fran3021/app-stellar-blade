from django.db import models
from usuarios.models import PerfilUsuario
from publicaciones.models import Publicacion, Comentario

class NotificacionPublicacion(models.Model):
    #notifica a todos los usuarios que sigue el creador de la publicacion
    destinatarios = models.ManyToManyField(PerfilUsuario, verbose_name='Destinatarios:', related_name='notificaciones_publicaciones')
    mensaje = models.CharField(verbose_name='Mensaje de la notificacion:', max_length=150)
    leida = models.BooleanField(verbose_name='¿Leida?:', default=False)
    url = models.URLField(verbose_name='URL de la nueva publicacion',null=True, blank=True)

    class Meta:
        verbose_name = 'Notificacion publicacion'
        verbose_name_plural = 'Notificacion publicaciones'

    def __str__(self):
        return f'{self.mensaje}'


class NotificacionResponderComentario(models.Model):
    #notifica al usuario que le han contestado un comentario
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name='Destinatario:', on_delete=models.CASCADE, related_name='notificaciones_comentarios')
    mensaje = models.CharField(verbose_name='Mensaje de la notificacion:', max_length=150)
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
