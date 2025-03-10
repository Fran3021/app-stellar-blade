from django.db import models
from usuarios.models import PerfilUsuario
from publicaciones.models import Publicacion, Comentario

class Notificacion (models.Model):
    destinatarios = models.ManyToManyField(PerfilUsuario, verbose_name='Destinatario:', related_name='notificaciones')
    mensaje = models.CharField(verbose_name='Mensaje de la notificacion:', max_length=150)
    leida = models.BooleanField(verbose_name='¿Leida?:', default=False)
    url = models.URLField(verbose_name='URL de la nueva publicacion',null=True, blank=True)

    class Meta:
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f'{self.mensaje}'