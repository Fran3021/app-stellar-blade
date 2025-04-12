from django.conf import settings
from .models import NotificacionPublicacion, NotificacionComentario, NotificacionSeguir, NotificacionRespuestaComentario, NotificacionMeGusta, NotificacionMensaje
from itertools import chain


def notificaciones_totales(request):
    if request.user.is_authenticated:
        notificaciones_publicacion = NotificacionPublicacion.objects.filter(destinatario=request.user.perfil).exclude(autor=request.user.perfil)

        notificaciones_comentarios = NotificacionComentario.objects.filter(destinatario=request.user.perfil).exclude(autor=request.user.perfil)

        notificaciones_seguir = NotificacionSeguir.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)

        notificaciones_respuesta_comentario = NotificacionRespuestaComentario.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)

        notificaciones_me_gusta = NotificacionMeGusta.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)

        notificaciones_mensajes = NotificacionMensaje.objects.filter(destinatario=request.user.perfil).exclude(usuario=request.user.perfil)

        for n in notificaciones_publicacion:
            n.tipo = 'publicacion'
        for n in notificaciones_comentarios:
            n.tipo = 'comentario'
        for n in notificaciones_seguir:
            n.tipo = 'seguir'
        for n in notificaciones_respuesta_comentario:
            n.tipo = 'respuesta_comentario'
        for n in notificaciones_me_gusta:
            n.tipo = 'me_gusta'
        for n in notificaciones_mensajes:
            n.tipo = 'mensaje'

        todas_las_notificaciones = list(chain(
            notificaciones_publicacion,
            notificaciones_comentarios,
            notificaciones_seguir,
            notificaciones_respuesta_comentario,
            notificaciones_me_gusta,
            notificaciones_mensajes,
        ))

        # Ordena por fecha_notificacion (del más reciente al más antiguo)
        todas_las_notificaciones.sort(key=lambda x: x.fecha_notificacion, reverse=True)
    else:
        todas_las_notificaciones = []

    return {
        'notificaciones_totales': todas_las_notificaciones,
    }