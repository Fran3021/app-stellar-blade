from django.shortcuts import render, redirect
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
from notificaciones.models import NotificacionSeguir
from stellarblade.forms import PerfilUsuarioForm

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
        context["publicaciones"] = Publicacion.objects.filter(autor = self.request.user.perfil).order_by('-fecha_publicacion')
        return context


@method_decorator(login_required, name='dispatch')
class UpdatePerfilView(UpdateView):
    template_name = 'usuarios/perfil_update.html'
    model = PerfilUsuario
    form_class = PerfilUsuarioForm

    def dispatch(self, request, *args, **kwargs):
        usuario_perfil = self.get_object()
        if usuario_perfil.usuario != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user#pasamos el usuario al formulario
        return kwargs

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


@method_decorator(login_required, name="dispatch")
class PublicacionesMisContactosView(ListView):
    model = Publicacion
    template_name = 'usuarios/publicaciones_mis_contactos.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #obtenemos el perfil de usuario logeado
        perfil_usuario = self.request.user.perfil
        #obtenemos a los usuarios que sigue el usuario logeado
        usuario_seguidos = perfil_usuario.seguidores.all()
        #lo filtramos para que salgan los que el autor de las publicaciones esten en los usuarios seguidos del usuario logeado
        context ["publicaciones"] = Publicacion.objects.filter(autor__in=usuario_seguidos).order_by('-fecha_publicacion')
        
        return context


@login_required
def follow_perfiles_ajax(request, pk):
    perfil = PerfilUsuario.objects.get(pk = pk)
    if Follow.objects.filter(seguidor = request.user.perfil, siguiendo = perfil).count():
        request.user.perfil.unfollow(perfil)
        NotificacionSeguir.objects.filter(destinatario=perfil, usuario=request.user.perfil, url=reverse_lazy('usuarios:detail', kwargs={'pk': request.user.perfil.pk})).delete()
        return JsonResponse({
            'mensaje': f'Se ha dejado de seguir al usuario {perfil.usuario}',
            'follow': False,
            'numero_seguidores': perfil.siguiendo.count()
        })
    else:
        request.user.perfil.follow(perfil)
        NotificacionSeguir.objects.create(destinatario=perfil, usuario=request.user.perfil, url=reverse_lazy('usuarios:detail', kwargs={'pk': request.user.perfil.pk}))
        return JsonResponse ({
            'mensaje': f'Se ha empezado a seguir al usuario {perfil.usuario}',
            'follow': True,
            'numero_seguidores': perfil.siguiendo.count()
        })


class PerfilesDetailView(DetailView):
    template_name = 'usuarios/perfiles_detail.html'
    model = PerfilUsuario
    context_object_name = 'perfil'

    def dispatch(self, request, *args, **kwargs):
        #evita que accedamos a detalle perfil del usuario logeado, nos redirige a nuestro perfil
        pk = self.kwargs.get('pk')
        usuario_perfil = PerfilUsuario.objects.get(pk=pk)
        if usuario_perfil.usuario == self.request.user:
            return redirect(reverse_lazy('usuarios:mi_perfil' , kwargs={'pk': pk}))
        return super().dispatch(request, *args, **kwargs)