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
from notificaciones.models import NotificacionPublicacion
from django.shortcuts import get_object_or_404

@method_decorator(login_required, name='dispatch')
class CrearPublicacionView(CreateView):
    template_name = 'publicaciones/publicacion_nueva.html'
    model = Publicacion
    form_class = CreatePublicacionForm

    def form_valid(self, form):
        nueva_publicacion = form.save(commit=False)
        nueva_publicacion.autor = self.request.user.perfil
        nueva_publicacion.save()
        titulo = nueva_publicacion.titulo
        perfil_usuario = self.request.user.perfil
        seguidores = perfil_usuario.seguidores.all()
        nueva_notificacion = NotificacionPublicacion.objects.create(mensaje = f'El usuario {perfil_usuario} ha escrito {titulo}' )
        nueva_notificacion.destinatarios.set(seguidores)
        nueva_notificacion.url = reverse_lazy('publicaciones:detalle', kwargs= {'pk': nueva_publicacion.pk})
        nueva_notificacion.save()
        messages.success(self.request, 'Publicacion creada correctamente')
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
        messages.success(self.request ,'Comentario añadido correctamente')
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
        'contenido',
    ]

    def dispatch(self, request, *args, **kwargs):
        usuario_perfil = self.get_object()
        if usuario_perfil.autor != self.request.user.perfil:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        messages.success(self.request, 'Publicacion editada correctamente')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('publicaciones:detalle', kwargs={'pk': self.object.pk})


def contestar_comentario_ajax(request, pk):
    if request.method == 'POST':
        comentario = get_object_or_404(Comentario, pk=pk)  
        respuesta = request.POST.get('respuesta')
        if respuesta:
            RespuestaComentario.objects.create(autor=request.user.perfil, comentario=comentario, respuesta=respuesta)

            return JsonResponse({
            'mensaje': f'Se ha contestado al comentario {comentario.pk}',
            'respuesta': respuesta,
            'autor': request.user.username,
            })
        else:
            return JsonResponse({
                'error': 'No puede enviar una respuesta vacia'
            }, status=400)



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
        publicacion.delete()
        messages.success(self.request, 'Publicacion eliminada correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('usuarios:mi_perfil', kwargs={'pk': self.request.user.perfil.pk})


@login_required
def like_ajax(request, pk):
    publicacion = Publicacion.objects.get(pk = pk)
    if request.user.perfil in publicacion.likes.all():
        request.user.perfil.unlike_pub(publicacion)
        return JsonResponse({
            'like': False,
            'mensaje': f'Se ha quitado el like en la siguiente publicacion: {publicacion.titulo}',
            'numero_likes': publicacion.likes.all().count()
        })
    else:
        request.user.perfil.like_pub(publicacion)
        return JsonResponse({
            'like': True,
            'mensaje': f'Se ha dado like en la siguiente publicacion: {publicacion.titulo}',
            'numero_likes': publicacion.likes.all().count()
        })
