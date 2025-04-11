from django.conf import settings
from .models import NotificacionPublicacion, NotificacionComentario, NotificacionSeguir, NotificacionRespuestaComentario, NotificacionMeGusta, NotificacionMensaje

def notificaciones_publicacion(request):
    if request.user.is_authenticated:
        notificaciones_publicacion = NotificacionPublicacion.objects.filter(destinatario=request.user.perfil).exclude(autor=request.user.perfil)
    else:
        notificaciones_publicacion = []

    return {
        'notificacion_publicacion': notificaciones_publicacion
    }

def notificaciones_comentario(request):
    if request.user.is_authenticated:
        notificaciones_comentarios = NotificacionComentario.objects.filter(destinatario=request.user.perfil).exclude(autor=request.user.perfil)
    else:
        notificaciones_comentarios = []

    return {
        'notificacion_comentarios': notificaciones_comentarios
    }

def notificaciones_seguir(request):
    if request.user.is_authenticated:
        notificaciones_seguir = NotificacionSeguir.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)
    else:
        notificaciones_seguir = []

    return {
        'notificacion_seguir': notificaciones_seguir
    }

def notificaciones_respuesta_comentario(request):
    if request.user.is_authenticated:
        notificaciones_respuesta_comentario = NotificacionRespuestaComentario.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)
    else:
        notificaciones_respuesta_comentario = []

    return {
        'notificacion_respuesta_comentario': notificaciones_respuesta_comentario
    }

def notificaciones_me_gusta(request):
    if request.user.is_authenticated:
        notificaciones_me_gusta = NotificacionMeGusta.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)
    else:
        notificaciones_me_gusta = []

    return {
        'notificacion_me_gusta': notificaciones_me_gusta
    }

def notificaciones_mensajes(request):
    if request.user.is_authenticated:
        notificaciones_mensajes = NotificacionMensaje.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)
    else:
        notificaciones_mensajes= []

    return {
        'notificacion_mensajes': notificaciones_mensajes
    }