from django.conf import settings
from .models import NotificacionPublicacion

def notificaciones_publicacion(request):
    if request.user.is_authenticated:
        notificaciones_publicacion = NotificacionPublicacion.objects.filter(destinatarios=request.user.perfil)
    else:
        notificaciones_publicacion = []

    return {
        'notificacion': notificaciones_publicacion
    }