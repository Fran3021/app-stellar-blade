from django.shortcuts import render, redirect
from .forms import RegisterForm, SearchForm
from django.views.generic import CreateView, FormView, ListView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from publicaciones.models import Publicacion, Comentario, RespuestaComentario
from usuarios.models import Follow, PerfilUsuario
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import PermissionDenied


class HomeView(ListView):
    template_name = 'general/home.html'
    model = Publicacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["publicaciones"] = Publicacion.objects.all().exclude(autor=self.request.user.perfil).order_by('-fecha_publicacion') 
        else:
            context["publicaciones"] = Publicacion.objects.all().order_by('-fecha_publicacion')
        return context

def legal_view(request):
    return render(request, 'general/legal.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada con exito')
    return HttpResponseRedirect(reverse_lazy('login'))

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'general/registro.html'
    success_url = reverse_lazy('login')


    #redirigimos al usuario a su perfil en caso de que este logeado
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            pk = self.request.user.perfil.pk
            return redirect(reverse_lazy('usuarios:mi_perfil' , kwargs={'pk': pk}))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado correctamente')
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'general/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    #redirigimos al usuario a su perfil en caso de que este logeado
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            pk = self.request.user.perfil.pk
            return redirect(reverse_lazy('usuarios:mi_perfil' , kwargs={'pk': pk}))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        recuerdame = self.request.POST.get('recuerdame')
        if recuerdame:
            self.request.session.set_expiry(1209600)

        #obtenemos el usuario y comprobamos que ese usuario y contraseña coincide con alguno en la base de datos
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Inicion de sesion exitoso.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Contraseña o usuario incorrectos.')
        return HttpResponseRedirect(reverse_lazy('login'))
        super().form_invalid(form)

@login_required
def search_view(request):
    if request.GET:
        formulario = SearchForm(request.GET)

        busqueda = formulario.data['value']#obtenemos lo que haya en el campo value del formulario

        publicaciones = Publicacion.objects.filter(titulo__icontains=busqueda)
        usuarios = PerfilUsuario.objects.filter(usuario__username__icontains=busqueda).exclude(usuario=request.user)# de esta forma accedemos al modelo PerfilUsuario para utilizar el include de _perfiles.html
        comentarios = Comentario.objects.filter(texto__icontains=busqueda)

        context ={
            'publicaciones': publicaciones,
            'usuarios': usuarios,
            'comentarios': comentarios,
            'formulario': formulario,
        }

        return render(request, 'general/busqueda.html', context)
    else:
        formulario = SearchForm()

        context = {
            'formulario': formulario
        }

        return render(request, 'general/busqueda.html', context)


#clase para personalizar los templates de recuperacion de contraseña
class PersonalizarReseteoContraseña(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'


def info_del_juego(request):
    return render(request, 'general/info_del_juego.html')

def politica_legal(request):
    return render(request, 'general/politica_legal.html')
