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


class NotificacionComentario(models.Model):
    autor = models.ForeignKey(PerfilUsuario, verbose_name='Autor:', on_delete=models.CASCADE, related_name='notificacion_comentario')
    publicacion = models.ForeignKey(Publicacion, verbose_name="Publicacion:", on_delete=models.CASCADE)
    #notifica al usuario que le han escrito un comentario
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name='Destinatario:', on_delete=models.CASCADE, related_name='notificaciones_comentarios')
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='URL de la publicacion comentada:',null=True, blank=True)

    class Meta:
        verbose_name = 'Notificacion comentario'
        verbose_name_plural = 'Notificacion comentarios'

    def __str__(self):
        return f'{self.autor} ha escrito un comentario en tu publicacion: {self.publicacion}'


class NotificacionSeguir(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, verbose_name='Usuario:', on_delete=models.CASCADE, related_name='notificacion_usuario')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name='Usuario que ha empezado a seguir:', on_delete=models.CASCADE, related_name='notificacion_destinatario')
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='url del perfil que empieza a seguir:', null=True, blank=True)

    def __str__(self):
        return f'El usuario {self.usuario} ha empezado a seguirte.'


class NotificacionRespuestaComentario(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, verbose_name="Autor que ha contestado:", on_delete=models.CASCADE, related_name='respuesta_usuario')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name="Autor del comentario:", on_delete=models.CASCADE, related_name='respuestas_destinatario')
    comentario = models.ForeignKey(Comentario, verbose_name='Comentario contestado:', on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, verbose_name="Publicacion que pertenece la respuesta:", on_delete=models.CASCADE)
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='url de la publicacion:', null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} ha contestado a tu comentario:{self.comentario}'


class NotificacionMeGusta(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, verbose_name="Usuario que ha dado me gusta:", on_delete=models.CASCADE, related_name='me_gusta_usuario')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name="Usuario al que pertenece la publicacion que le ha dado a me gusta:", on_delete=models.CASCADE, related_name='me_gusta_destinatario')
    publicacion = models.ForeignKey(Publicacion, verbose_name="Publicacion que pertenece el me gusta:", on_delete=models.CASCADE)
    leida = models.BooleanField(verbose_name='¿Leida?', default=False)
    url = models.URLField(verbose_name='url de la publicacion:', null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} ha dado a me gusta a tu publicacion:{self.publicacion}'