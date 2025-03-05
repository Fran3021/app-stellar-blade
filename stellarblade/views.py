from django.shortcuts import render
from .forms import RegisterForm
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse, reverse_lazy


def home_view(request):
    return render(request, 'general/home.html')

def legal_view(request):
    return render(request, 'general/legal.html')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'general/registro.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado correctamente')
        return super().form_valid(form)


