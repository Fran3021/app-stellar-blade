from django.conf import settings
from .models import NotificacionPublicacion, NotificacionComentario, NotificacionSeguir

def notificaciones_publicacion(request):
    if request.user.is_authenticated:
        notificaciones_publicacion = NotificacionPublicacion.objects.filter(destinatarios=request.user.perfil, leida=True)
    else:
        notificaciones_publicacion = []

    return {
        'notificacion': notificaciones_publicacion
    }

def notificaciones_comentario(request):
    if request.user.is_authenticated:
        notificaciones_comentarios = NotificacionComentario.objects.filter(destinatario=request.user.perfil)
    else:
        notificaciones_comentarios = []

    return {
        'notificacion': notificaciones_comentarios
    }