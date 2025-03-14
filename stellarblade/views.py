from django.shortcuts import render
from .forms import RegisterForm
from django.views.generic import CreateView, FormView, ListView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from usuarios.models import Follow



class HomeView(ListView):
    template_name = 'general/home.html'
    model = Publicacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            #obtenemos el perfil de usuario logeado
            perfil_usuario = self.request.user.perfil
            #obtenemos a los usuarios que sigue el usuario logeado
            usuario_seguidos = perfil_usuario.seguidores.all()
            #lo filtramos para que salgan los que el autor de las publicaciones esten en los usuarios seguidos del usuario logeado
            context ["publicaciones"] = Publicacion.objects.filter(autor__in=usuario_seguidos).order_by('-fecha_publicacion')
        else:
            context["publicaciones"] = Publicacion.objects.all().order_by('-fecha_publicacion') 
        
        return context

def legal_view(request):
    return render(request, 'general/legal.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada con exito')
    return HttpResponseRedirect(reverse_lazy('login'))

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'general/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado correctamente')
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'general/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Inicion de sesion exitoso.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Contraseña o usuario incorrectos.')
        return HttpResponseRedirect(reverse_lazy('login'))
        super().form_invalid(form)




