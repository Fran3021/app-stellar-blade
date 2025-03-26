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
from notificaciones.models import NotificacionPublicacion, NotificacionComentario, NotificacionRespuestaComentario, NotificacionMeGusta, NotificacionSeguir
from .models import Mensaje, Conversacion
from .forms import CreateMensajeForm
from django.shortcuts import get_object_or_404
from django.db.models import Q


class CreateMensajeView(CreateView):
    template_name = 'mensajes/nuevo_mensaje.html'
    model = Mensaje
    form_class = CreateMensajeForm

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        destinatario = PerfilUsuario.objects.get(pk = pk)
        conversacion = Conversacion.objects.create(usuario1=self.request.user.perfil, usuario2 = destinatario)
        form.instance.autor = self.request.user.perfil
        form.instance.destinatario = destinatario
        form.instance.conversacion = conversacion

        messages.success(self.request, 'Mensaje enviado correctamente')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mensajes:conversaciones')



class ConversacionesView(ListView):
    template_name = 'mensajes/conversaciones.html'
    model = Conversacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mensajes"] = Mensaje.objects.filter(
            Q(autor = self.request.user.perfil) | Q(destinatario = self.request.user.perfil)
            )
        
        return context