from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView, ListView
from usuarios.models import PerfilUsuario, Follow
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import NotificacionPublicacion, NotificacionComentario, NotificacionRespuestaComentario, NotificacionMeGusta, NotificacionSeguir, NotificacionMensaje
from django.shortcuts import get_object_or_404

@login_required
def list_notificaciones(request):
    return render(request, 'notificaciones/notificaciones.html')


@login_required
def marcar_notificacion_leida_comentario(request, pk):
    notificacion = NotificacionComentario.objects.get(pk = pk)
    if notificacion:
        notificacion.leida = True
        notificacion.save()
        return JsonResponse({
            'success': True,
            'mensaje': 'Notificacion leida correctamente'
        })
    else:
        return JsonResponse({
            'success': False,
            'mensaje': 'Notificacion no encontrada'
        })


@login_required
def marcar_notificacion_leida_publicacion(request, pk):
    notificacion = NotificacionPublicacion.objects.get(pk = pk)
    if notificacion:
        notificacion.leida = True
        notificacion.save()
        return JsonResponse({
            'success': True,
            'mensaje': 'Notificacion leida correctamente'
        })
    else:
        return JsonResponse({
            'success': False,
            'mensaje': 'Notificacion no encontrada'
        })


@login_required
def marcar_notificacion_leida_respuesta_comentario(request, pk):
    notificacion = NotificacionRespuestaComentario.objects.get(pk = pk)
    if notificacion:
        notificacion.leida = True
        notificacion.save()
        return JsonResponse({
            'success': True,
            'mensaje': 'Notificacion leida correctamente'
        })
    else:
        return JsonResponse({
            'success': False,
            'mensaje': 'Notificacion no encontrada'
        })


@login_required
def marcar_notificacion_leida_me_gusta(request, pk):
    notificacion = NotificacionMeGusta.objects.get(pk = pk)
    if notificacion:
        notificacion.leida = True
        notificacion.save()
        return JsonResponse({
            'success': True,
            'mensaje': 'Notificacion leida correctamente'
        })
    else:
        return JsonResponse({
            'success': False,
            'mensaje': 'Notificacion no encontrada'
        })


@login_required
def marcar_notificacion_leida_seguir(request, pk):
    notificacion = NotificacionSeguir.objects.get(pk = pk)
    if notificacion:
        notificacion.leida = True
        notificacion.save()
        return JsonResponse({
            'success': True,
            'mensaje': 'Notificacion leida correctamente'
        })
    else:
        return JsonResponse({
            'success': False,
            'mensaje': 'Notificacion no encontrada'
        })



@login_required
def marcar_notificacion_leida_mensajes(request, pk):
    notificacion = NotificacionMensaje.objects.get(pk = pk)
    if notificacion:
        notificacion.leida = True
        notificacion.save()
        return JsonResponse({
            'success': True,
            'mensaje': 'Notificacion leida correctamente'
        })
    else:
        return JsonResponse({
            'success': False,
            'mensaje': 'Notificacion no encontrada'
        })


