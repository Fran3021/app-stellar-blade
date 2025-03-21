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
from .models import NotificacionPublicacion, NotificacionComentario, NotificacionRespuestaComentario, NotificacionMeGusta
from django.shortcuts import get_object_or_404


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


