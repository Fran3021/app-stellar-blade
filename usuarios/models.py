from django.db import models
from django.contrib.auth.models import User



class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, verbose_name='Usuario:', on_delete=models.CASCADE, related_name='perfil')
    imagen_perfil = models.ImageField(verbose_name='Imagen de perfil:', upload_to='usuarios/img_perfil/', null=True, blank=True)
    biografia = models.TextField(verbose_name='Biografia del ususario:', max_length=300, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento:', null=True, blank=True, default='1900-01-01')
    seguidores = models.ManyToManyField('self', verbose_name='Seguidores', symmetrical=False, related_name='siguiendo', through='Follow')

    def follow(self, perfil):
        Follow.objects.get_or_create(seguidor = self, siguiendo = perfil)

    def unfollow(self, perfil):
        Follow.objects.filter(seguidor = self,  siguiendo = perfil).delete()

    def like_pub(self, publicacion):
        publicacion.like(self)
    
    def unlike_pub(self, publicacion):
        publicacion.unlike(self)

    def total_notificaciones(self):
        from notificaciones.models import NotificacionComentario, NotificacionPublicacion, NotificacionSeguir, NotificacionRespuestaComentario, NotificacionMeGusta, NotificacionMensaje
        
        notificaciones_comentario = NotificacionComentario.objects.filter(destinatario=self).filter(leida=False).count()
        notificaciones_publicacion = NotificacionPublicacion.objects.filter(destinatario=self).filter(leida=False).count()
        notificaciones_seguir = NotificacionSeguir.objects.filter(destinatario=self).filter(leida=False).count()
        notificaciones_respuestas_comentario = NotificacionRespuestaComentario.objects.filter(destinatario=self).filter(leida=False).count()
        notificaciones_me_gusta = NotificacionMeGusta.objects.filter(destinatario=self).filter(leida=False).count()
        notificaciones_mensajes = NotificacionMensaje.objects.filter(destinatario=self).filter(leida=False).count()
        
        return notificaciones_comentario + notificaciones_publicacion + notificaciones_seguir + notificaciones_respuestas_comentario + notificaciones_me_gusta + notificaciones_mensajes
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.usuario.username


class Follow(models.Model):
    seguidor = models.ForeignKey(PerfilUsuario, verbose_name='Seguidor', on_delete=models.CASCADE, related_name='siguiendo_set')
    siguiendo = models.ForeignKey(PerfilUsuario, verbose_name='Siguiendo', on_delete=models.CASCADE, related_name='seguidores_set')
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de inicio', auto_now_add=True)

    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'
        unique_together = ('seguidor', 'siguiendo')#nos aseguramos que solo se siga una vez cada seguidor y seguido

    def __str__(self):
        return f'El usuario: {self.seguidor} sigue a: {self.siguiendo}, con fecha de inicio: {self.fecha_inicio}'


