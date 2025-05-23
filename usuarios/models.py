from django.db import models
from django.contrib.auth.models import User
from thumbnails.fields import ImageField
from django.utils.translation import gettext_lazy as _



class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, verbose_name='Usuario:', on_delete=models.CASCADE, related_name='perfil')
    imagen_perfil = ImageField(verbose_name=_('Imagen de perfil:'), upload_to='usuarios/img_perfil/', null=True, blank=True)
    biografia = models.TextField(verbose_name=_('Biografia del ususario:'), max_length=300, blank=True)
    fecha_nacimiento = models.DateField(verbose_name=_('Fecha de nacimiento:'), null=True, blank=True, default='1900-01-01')
    seguidores = models.ManyToManyField('self', verbose_name='Seguidores', symmetrical=False, related_name='siguiendo', through='Follow')

    def follow(self, perfil):
        Follow.objects.get_or_create(seguidor = self, siguiendo = perfil)

    def unfollow(self, perfil):
        Follow.objects.filter(seguidor = self,  siguiendo = perfil).delete()

    def like_pub(self, publicacion):
        publicacion.like(self)
    
    def unlike_pub(self, publicacion):
        publicacion.unlike(self)

    #funcion que devuelve el numero total de notificaciones del usuario logeado
    def total_notificaciones(self):
        from notificaciones.models import NotificacionComentario, NotificacionPublicacion, NotificacionSeguir, NotificacionRespuestaComentario, NotificacionMeGusta, NotificacionMensaje
        
        notificaciones_comentario = NotificacionComentario.objects.filter(destinatario=self).filter(leida=False).exclude(autor=self).count()
        notificaciones_publicacion = NotificacionPublicacion.objects.filter(destinatario=self).filter(leida=False).exclude(autor=self).count()
        notificaciones_seguir = NotificacionSeguir.objects.filter(destinatario=self).filter(leida=False).exclude(usuario=self).count()
        notificaciones_respuestas_comentario = NotificacionRespuestaComentario.objects.filter(destinatario=self).filter(leida=False).exclude(usuario=self).count()
        notificaciones_me_gusta = NotificacionMeGusta.objects.filter(destinatario=self).filter(leida=False).exclude(usuario=self).count()
        notificaciones_mensajes = NotificacionMensaje.objects.filter(destinatario=self).filter(leida=False).exclude(usuario=self).count()
        
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


