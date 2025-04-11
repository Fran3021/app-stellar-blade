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
from notificaciones.models import NotificacionPublicacion, NotificacionComentario, NotificacionRespuestaComentario, NotificacionMeGusta, NotificacionSeguir, NotificacionMensaje
from .models import Mensaje, Conversacion
from .forms import CreateMensajeForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

@method_decorator(login_required, name='dispatch')
class CreateMensajeView(CreateView):
    template_name = 'mensajes/nuevo_mensaje.html'
    model = Mensaje
    form_class = CreateMensajeForm


    def dispatch(self, request, *args, **kwargs):
        #en caso de que se intente mandar un mensaje a si mismo, no nos deja
        pk = self.kwargs.get('pk')
        usuario_perfil = PerfilUsuario.objects.get(pk=pk)
        if usuario_perfil.usuario == self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        pk = self.kwargs.get('pk')#obtenemos el pk de la url, que guardamos antes que corresponde al perfil que estemos viendo
        destinatario = PerfilUsuario.objects.get(pk = pk)
        conversacion = Conversacion.objects.create(usuario1=self.request.user.perfil, usuario2 = destinatario)
        nuevo_mensaje = form.save(commit=False)
        nuevo_mensaje.autor = self.request.user.perfil
        nuevo_mensaje.destinatario = destinatario
        nuevo_mensaje.conversacion = conversacion
        nuevo_mensaje.save()

        NotificacionMensaje.objects.create(destinatario=destinatario, usuario=self.request.user.perfil, mensaje=nuevo_mensaje, conversacion=conversacion, url= reverse_lazy('mensajes:conversaciones_detail', kwargs={'pk': conversacion.pk}))

        messages.success(self.request, 'Mensaje enviado correctamente')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mensajes:conversaciones')


@method_decorator(login_required, name='dispatch')
class ConversacionesView(ListView):
    template_name = 'mensajes/conversaciones.html'
    model = Conversacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conversaciones"] = Conversacion.objects.filter(
            Q(usuario1 = self.request.user.perfil) | Q(usuario2 = self.request.user.perfil)
            )
        
        return context


@method_decorator(login_required, name='dispatch')
class ConversacionesDetailView(DetailView):
    template_name = 'mensajes/conversaciones_detail.html'
    model = Conversacion
    context_object_name = 'conversacion'


@login_required
def contestar_mensaje(request, pk):
    if request.method == 'POST':
        mensaje = Mensaje.objects.get(pk = pk)

        conversacion = Conversacion.objects.filter(
            usuario1=mensaje.autor, usuario2=mensaje.destinatario
        ).first() or Conversacion.objects.filter(
            usuario1=mensaje.destinatario, usuario2=mensaje.autor
        ).first()

        if not conversacion:
            return JsonResponse({'success': False, 'error': 'Conversación no encontrada'})
        

        respuesta_mensaje = request.POST.get('contenido')
        if respuesta_mensaje:

            autor_mensaje = request.user.perfil

            destinatario_respuesta = (
                conversacion.usuario1 if autor_mensaje == conversacion.usuario2 else conversacion.usuario2
            )
            mensaje_respuesta = Mensaje.objects.create(conversacion=conversacion, autor=autor_mensaje, destinatario=destinatario_respuesta, contenido=respuesta_mensaje)

            NotificacionMensaje.objects.create(destinatario=destinatario_respuesta, usuario=autor_mensaje, mensaje=mensaje_respuesta, conversacion=conversacion, url= reverse_lazy('mensajes:conversaciones_detail', kwargs={'pk': conversacion.pk}))
            
            return JsonResponse({
                'success': True
            })
        else:
            return JsonResponse({
                'success': False
            })


@login_required
def eliminar_mensaje(request, pk):
    if request.method == 'DELETE':
        mensaje = Mensaje.objects.get(pk = pk)
        conversacion = Conversacion.objects.get(pk = mensaje.conversacion.pk)
        if request.user.perfil == mensaje.autor:
            notificacion = NotificacionMensaje.objects.filter(destinatario=mensaje.destinatario, usuario=mensaje.autor, conversacion=conversacion, mensaje=mensaje).first()
            notificacion.delete()
            mensaje.delete()
            return JsonResponse({
                'success': True,
                'message': 'Mensaje eliminado corectamente',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No se ha podido borrar el mensaje',
            })


@login_required
def eliminar_conversacion(request, pk):
    if request.method == 'DELETE':
        conversacion = Conversacion.objects.get(pk = pk)
        perfil_usuario = request.user.perfil
        if conversacion.usuario1 == perfil_usuario or conversacion.usuario2 == perfil_usuario:
            conversacion.delete()
            return JsonResponse({
                'success': True,
                'message': 'Conversacion eliminida correctamente',
            })
        else:
            return JsonResponse({
                'success': True,
                'message': 'No se ha podido eliminar la conversacion',
            })
