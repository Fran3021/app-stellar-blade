from django.db import models
from usuarios.models import PerfilUsuario
from django.utils.translation import gettext_lazy as _

class Conversacion(models.Model):
    usuario1 = models.ForeignKey(PerfilUsuario, verbose_name="Usuario1:", on_delete=models.CASCADE, related_name='conversaciones_user1')
    usuario2 = models.ForeignKey(PerfilUsuario, verbose_name="Usuario2:", on_delete=models.CASCADE, related_name='conversaciones_user2')
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de inicio de la conversacion:', auto_now_add=True)

    class Meta:
        unique_together = ('usuario1', 'usuario2')#nos aseguramos que no se repita
        verbose_name = 'Conversacion'
        verbose_name_plural = 'Conversaciones'

    #lo ponemos de esta forma para que se pueda traducir sin problemas
    def __str__(self):
        return _('Conversación entre %(u1)s y %(u2)s') % {
            'u1': self.usuario1,
            'u2': self.usuario2
        }


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, verbose_name="Conversacion a la que pertenece:", on_delete=models.CASCADE, related_name='mensajes')
    autor = models.ForeignKey(PerfilUsuario, verbose_name="Usuario que envia el mensaje:", on_delete=models.CASCADE, related_name='autor_mensaje')
    destinatario = models.ForeignKey(PerfilUsuario, verbose_name="Usuario que recibe el mensaje", on_delete=models.CASCADE, related_name='destinatario_mensaje')
    contenido = models.CharField(verbose_name=_("Contenido del mensaje:"), max_length=150)
    fecha_mensaje = models.DateTimeField(verbose_name="Fecha del mensaje:", auto_now_add=True)
    leido = models.BooleanField(verbose_name='¿Leido?', default=False)

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f'{self.contenido}'