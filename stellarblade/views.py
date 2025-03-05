from django.shortcuts import render
from .forms import RegisterForm
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect


def home_view(request):
    return render(request, 'general/home.html')

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




