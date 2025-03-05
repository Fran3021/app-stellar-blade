from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView
from .models import PerfilUsuario
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

class MyPerfilView(DetailView):
    model = PerfilUsuario
    template_name = 'usuarios/mi_perfil.html'

    def dispatch(self, request, *args, **kwargs):
        usuario_perfil = self.get_object()
        if usuario_perfil.usuario != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["perfil"] = PerfilUsuario.objects.get(pk=self.object.pk)
        return context


class UpdatePerfilView(UpdateView):
    template_name = 'usuarios/perfil_update.html'
    model = PerfilUsuario
    fields = [
        'imagen_perfil',
        'biografia',
        'fecha_nacimiento',
    ]


    def dispatch(self, request, *args, **kwargs):
        usuario_perfil = self.get_object()
        if usuario_perfil.usuario != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        messages.success(self.request, 'Usuario editado correctamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('usuarios:mi_perfil', kwargs={'pk': self.object.pk})


class DeletePerfilView(DeleteView):
    model = PerfilUsuario
    template_name = 'usuarios/perfil_delete.html'
    success_url = reverse_lazy('registro')

    def dispatch(self, request, *args, **kwargs):
        usuario_perfil = self.get_object()
        if usuario_perfil.usuario != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        usuario = User.objects.get(username = self.object.usuario)
        usuario.delete()
        messages.success(self.request, 'Perfil eliminado correctamente')
        return super().form_valid(form)