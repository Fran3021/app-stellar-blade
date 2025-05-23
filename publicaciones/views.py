from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView, ListView
from usuarios.models import PerfilUsuario, Follow
from .models import Publicacion, Comentario, RespuestaComentario
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import CreatePublicacionForm, CreateComentarioForm, ContestarComentarioForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from notificaciones.models import NotificacionPublicacion, NotificacionComentario, NotificacionRespuestaComentario, NotificacionMeGusta
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


@method_decorator(login_required, name='dispatch')
class CrearPublicacionView(CreateView):
    template_name = 'publicaciones/publicacion_nueva.html'
    model = Publicacion
    form_class = CreatePublicacionForm

    def form_valid(self, form):
        nueva_publicacion = form.save(commit=False)
        nueva_publicacion.autor = self.request.user.perfil
        nueva_publicacion.save()#nos aseguramos de redirigir al usuario a la nueva publicacion creada en succes_url
        titulo = nueva_publicacion.titulo
        perfil_usuario = self.request.user.perfil
        seguidores = perfil_usuario.siguiendo.all()
        for seguidor in seguidores:
            NotificacionPublicacion.objects.create(autor=perfil_usuario, publicacion=nueva_publicacion, destinatario=seguidor, url= reverse_lazy('publicaciones:detalle', kwargs= {'pk': nueva_publicacion.pk}))

        messages.success(self.request, _('Publicacion creada correctamente'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('publicaciones:detalle', kwargs={'pk': self.object.pk})


class DetailPublicacionView(DetailView, CreateView):
    template_name = 'publicaciones/publicacion_detail.html'
    model = Publicacion
    context_object_name = 'publicacion'
    form_class = CreateComentarioForm

    def form_valid(self, form):
        form.instance.publicacion = self.get_object()
        form.instance.autor = self.request.user.perfil
        perfil_usuario = self.request.user.perfil
        publicacion = self.get_object()
        destinatario = publicacion.autor
        if self.request.user.perfil != publicacion.autor:
            NotificacionComentario.objects.create(autor=perfil_usuario, destinatario=destinatario, publicacion=publicacion, url=reverse_lazy('publicaciones:detalle', kwargs= {'pk': publicacion.pk}))
        messages.success(self.request ,_('Comentario añadido correctamente'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('publicaciones:detalle', args=[self.get_object().pk])


@method_decorator(login_required, name='dispatch')
class UpdatePublicacionView(UpdateView):
    template_name = 'publicaciones/publicacion_update.html'
    model = Publicacion
    fields = [
        'titulo',
        'imagen',
        'video',
        'contenido',
    ]

    #solo se puede editar si el usuario logeado es el autor de la publicacion
    def dispatch(self, request, *args, **kwargs):
        usuario_perfil = self.get_object()
        if usuario_perfil.autor != self.request.user.perfil:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        messages.success(self.request, _('Publicacion editada correctamente'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('publicaciones:detalle', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class DeletePublicacionView(DeleteView):
    template_name = 'publicaciones/publicacion_delete.html'
    model = Publicacion

    def dispatch(self, request, *args, **kwargs):
        usuario_perfil = self.get_object()
        if usuario_perfil.autor != self.request.user.perfil:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        publicacion = Publicacion.objects.get(pk = self.object.pk)
        NotificacionPublicacion.objects.filter(publicacion=publicacion).delete()
        publicacion.delete()
        messages.success(self.request, _('Publicacion eliminada correctamente.'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('usuarios:mi_perfil', kwargs={'pk': self.request.user.perfil.pk})


@login_required
def contestar_comentario_ajax(request, pk):
    if request.method == 'POST':
        comentario = get_object_or_404(Comentario, pk=pk)  
        respuesta = request.POST.get('respuesta')
        pkPublicacion = request.POST.get('publicacion_pk')
        publicacion = Publicacion.objects.get(pk=pkPublicacion)
        if respuesta:
            RespuestaComentario.objects.create(autor=request.user.perfil, publicacion=publicacion, comentario=comentario, respuesta=respuesta)

            NotificacionRespuestaComentario.objects.create(comentario=comentario, destinatario=comentario.autor, usuario=request.user.perfil, publicacion=publicacion, url=reverse_lazy('publicaciones:detalle', kwargs={'pk': pkPublicacion}))

            return JsonResponse({
            'mensaje': _('Se ha contestado al comentario de: %(autor)s') % {
                'autor': comentario.autor
            },
            'respuesta': respuesta,
            'autor': request.user.username,
            })
        else:
            return JsonResponse({
            'mensaje': _('No se ha podido contestar al comentario de: %(autor)s') % {
                'autor': comentario.autor
            }
            })


@login_required
def like_ajax(request, pk):
    publicacion = Publicacion.objects.get(pk = pk)
    if request.user.perfil in publicacion.likes.all():
        request.user.perfil.unlike_pub(publicacion)
        NotificacionMeGusta.objects.filter(publicacion=publicacion, destinatario=publicacion.autor, usuario=request.user.perfil, url= reverse_lazy('publicaciones:detalle', kwargs={'pk': publicacion.pk})).delete()
        return JsonResponse({
            'like': False,
            'mensaje': _('Se ha quitado like en la siguiente publicacion: %(publicacion)s') % {
                'publicacion': publicacion.titulo
            },
            'numero_likes': publicacion.likes.all().count()
        })
    else:
        request.user.perfil.like_pub(publicacion)
        if request.user.perfil != publicacion.autor:
            NotificacionMeGusta.objects.create(publicacion=publicacion, destinatario=publicacion.autor, usuario=request.user.perfil, url= reverse_lazy('publicaciones:detalle', kwargs={'pk': publicacion.pk}))
        return JsonResponse({
            'like': True,
            'mensaje': _('Se ha dado like a la siguiente publicacion: %(publicacion)s') % {
                'publicacion': publicacion.titulo
            },
            'numero_likes': publicacion.likes.all().count()
        })


@login_required
def eliminar_comentario(request, pk):
    if request.method == 'DELETE':
        comentario = Comentario.objects.get(pk = pk)
        if request.user.perfil == comentario.autor:
            NotificacionComentario.objects.filter(autor=comentario.autor, publicacion=comentario.publicacion).delete()
            comentario.delete()
            return JsonResponse({
                'success': True,
                'mensaje': _('Se ha eliminado el comentario')
            })
        else:
            return JsonResponse({
                'success': False,
                'mensaje': _('No se ha podido eliminar el comentario')
            })


@login_required
def eliminar_respuesta_comentario(request, pk):
    if request.method == 'DELETE':
        respuesta_comentario = RespuestaComentario.objects.get(pk = pk)
        if request.user.perfil == respuesta_comentario.autor:
            NotificacionRespuestaComentario.objects.filter(usuario=respuesta_comentario.autor, publicacion=respuesta_comentario.publicacion).delete()
            respuesta_comentario.delete()
            return JsonResponse({
                'success': True,
                'mensaje': _('Se ha eliminado la respuesta'),
            })
        else:
            return JsonResponse({
                'success': False,
                'mensaje': _('No se ha podido eliminar la respuesta'),
            })


