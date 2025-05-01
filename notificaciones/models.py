from django.db import models
from usuarios.models import PerfilUsuario
from publicaciones.models import Publicacion, Comentario
from mensajes.models import Mensaje, Conversacion
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class NotificacionPublicacion(models.Model):
    autor = models.ForeignKey(PerfilUsuario, verbose_name='Autor:', on_delete=models.CASCADE, related_name='notificacion_publicacion')
    publicacion = models.ForeignKey(Publicacion, verbose_name="Publicacion:", on_delete=models.CASCADE)
    #notifica a todos los usuarios que sigue el creador de la publicacion
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name='Destinatario:', on_delete=models.CASCADE, related_name='notificaciones_publicaciones')
    leida = models.BooleanField(verbose_name='¿Leida?:', default=False)
    url = models.URLField(verbose_name='URL de la nueva publicacion',null=True, blank=True)
    fecha_notificacion = models.DateTimeField(verbose_name="Fecha notificacion:", auto_now_add=True)

    class Meta:
        verbose_name = 'Notificacion publicacion'
        verbose_name_plural = 'Notificaciones de publicaciones'

    def __str__(self):
        return _('%(autor)s ha publicado una nueva publicacion: %(publicacion)s') % {
            'autor': self.autor,
            'publicacion': self.publicacion,
        }


class NotificacionComentario(models.Model):
    autor = models.ForeignKey(PerfilUsuario, verbose_name='Autor:', on_delete=models.CASCADE, related_name='notificacion_comentario')
    publicacion = models.ForeignKey(Publicacion, verbose_name="Publicacion:", on_delete=models.CASCADE)
    #notifica al usuario que le han escrito un comentario
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name='Destinatario:', on_delete=models.CASCADE, related_name='notificaciones_comentarios')
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='URL de la publicacion comentada:',null=True, blank=True)
    fecha_notificacion = models.DateTimeField(verbose_name="Fecha notificacion:", auto_now_add=True)

    class Meta:
        verbose_name = 'Notificacion comentario'
        verbose_name_plural = 'Notificaciones de comentarios'

    def __str__(self):
        return _('%(autor)s ha escrito un comentario en tu publicacion: %(publicacion)s') % {
            'autor': self.autor,
            'publicacion': self.publicacion,
        }


class NotificacionSeguir(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, verbose_name='Usuario:', on_delete=models.CASCADE, related_name='notificacion_usuario')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name='Usuario que ha empezado a seguir:', on_delete=models.CASCADE, related_name='notificacion_destinatario')
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='url del perfil que empieza a seguir:', null=True, blank=True)
    fecha_notificacion = models.DateTimeField(verbose_name="Fecha notificacion:", auto_now_add=True)

    class Meta:
        verbose_name = 'Notificacion seguir'
        verbose_name_plural = 'Notificaciones de seguir'

    def __str__(self):
        return _('El usuario %(usuario)s ha empezado a seguirte.') % {
            'usuario': self.usuario
        }


class NotificacionRespuestaComentario(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, verbose_name="Autor que ha contestado:", on_delete=models.CASCADE, related_name='respuesta_usuario')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name="Autor del comentario:", on_delete=models.CASCADE, related_name='respuestas_destinatario')
    comentario = models.ForeignKey(Comentario, verbose_name='Comentario contestado:', on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, verbose_name="Publicacion que pertenece la respuesta:", on_delete=models.CASCADE)
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='url de la publicacion:', null=True, blank=True)
    fecha_notificacion = models.DateTimeField(verbose_name="Fecha notificacion:", auto_now_add=True)

    class Meta:
        verbose_name = 'Notificacion de respuesta a comentario'
        verbose_name_plural = 'Notificaciones de respuestas a comentarios'

    def __str__(self):
        return _('%(usuario)s ha contestado a tu comentario: %(comentario)s') % {
            'usuario': self.usuario,
            'comentario': self.comentario,
        }


class NotificacionMeGusta(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, verbose_name="Usuario que ha dado me gusta:", on_delete=models.CASCADE, related_name='me_gusta_usuario')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name="Usuario al que pertenece la publicacion que le ha dado a me gusta:", on_delete=models.CASCADE, related_name='me_gusta_destinatario')
    publicacion = models.ForeignKey(Publicacion, verbose_name="Publicacion que pertenece el me gusta:", on_delete=models.CASCADE)
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='url de la publicacion:', null=True, blank=True)
    fecha_notificacion = models.DateTimeField(verbose_name="Fecha notificacion:", auto_now_add=True)
    class Meta:
        verbose_name = 'Notificacion de me gusta'
        verbose_name_plural = 'Notificaciones de me gusta'

    def __str__(self):
        return _('%(usuario)s ha dado a me gusta a tu publicacion:%(publicacion)s') % {
            'usuario': self.usuario,
            'publicacion': self.publicacion,
        }


class NotificacionMensaje(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, verbose_name='Usuario que envia el mensaje:', on_delete=models.CASCADE, related_name='mensajes_usuarios')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name='Usuario que recibe el mensaje:', on_delete=models.CASCADE, related_name='mensajes_destinatario')
    mensaje = models.ForeignKey(Mensaje, verbose_name='Mensaje:', on_delete=models.CASCADE)
    conversacion = models.ForeignKey(Conversacion, verbose_name='Conversacion que pertenece el mensaje:', on_delete=models.CASCADE)
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='URL de la conversacion', null=True, blank=True)
    fecha_notificacion = models.DateTimeField(verbose_name="Fecha notificacion:", auto_now_add=True)

    class Meta:
        verbose_name = 'Notificacion de mensaje'
        verbose_name_plural = 'Notificaciones de mensajes'

    def __str__(self):
        return _('%(usuario)s te ha enviado un mensaje') % {
            'usuario': self.usuario,
        }