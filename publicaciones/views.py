from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView, ListView
from usuarios.models import PerfilUsuario, Follow
from .models import Publicacion
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import CreatePublicacionForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class CrearPublicacionView(CreateView):
    template_name = 'publicaciones/publicacion_nueva.html'
    model = Publicacion
    form_class = CreatePublicacionForm

    def form_valid(self, form):
        form.instance.autor = self.request.user.perfil
        messages.success(self.request, 'Publicacion creada correctamente')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('usuarios:mi_perfil', kwargs={'pk': self.request.user.perfil.pk})


class DetailPublicacionView(DetailView):
    template_name = 'publicaciones/publicacion_detail.html'
    model = Publicacion
    context_object_name = 'publicacion'


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
        return reverse_lazy('usuarios:mi_perfil', kwargs={'pk': self.object.pk})
