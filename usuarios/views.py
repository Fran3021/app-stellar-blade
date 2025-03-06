from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView, ListView
from .models import PerfilUsuario, Follow
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
from publicaciones.models import Publicacion
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
        context["publicaciones"] = Publicacion.objects.filter(autor = self.request.user.perfil)
        return context


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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


class ListPerfilesViews(ListView):
    model = PerfilUsuario
    template_name = 'usuarios/perfiles_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["perfiles"] = PerfilUsuario.objects.all().exclude(usuario = self.request.user)
        else:
            context["perfiles"] = PerfilUsuario.objects.all()
        
        return context

@login_required
def follow_perfiles_ajax(request, pk):
    perfil = PerfilUsuario.objects.get(pk = pk)
    if Follow.objects.filter(seguidor = request.user.perfil, siguiendo = perfil).count():
        request.user.perfil.unfollow(perfil)
        return JsonResponse({
            'mensaje': f'Se ha dejado de seguir al usuario {perfil.usuario}',
            'follow': False,
            'numero_seguidores': perfil.siguiendo.count()
        })
    else:
        request.user.perfil.follow(perfil)
        return JsonResponse ({
            'mensaje': f'Se ha empezado a seguir al usuario {perfil.usuario}',
            'follow': True,
            'numero_seguidores': perfil.siguiendo.count()
        })


class PerfilesDetailView(DetailView):
    template_name = 'usuarios/perfiles_detail.html'
    model = PerfilUsuario
    context_object_name = 'perfil'