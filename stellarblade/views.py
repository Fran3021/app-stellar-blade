from django.shortcuts import render
from .forms import RegisterForm
from django.views.generic import CreateView


def home_view(request):
    return render(request, 'general/home.html')

def legal_view(request):
    return render(request, 'general/legal.html')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'general/registro.html'


