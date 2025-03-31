"""
URL configuration for stellarblade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import CreateMensajeView, ConversacionesView, ConversacionesDetailView, contestar_mensaje, eliminar_mensaje, eliminar_conversacion


app_name = 'mensajes'

urlpatterns = [
    path('conversaciones/', ConversacionesView.as_view(), name = 'conversaciones'),
    path('conversaciones-detail/<pk>', ConversacionesDetailView.as_view(), name = 'conversaciones_detail'),
    path('nuevo/<pk>/', CreateMensajeView.as_view(), name = 'nuevo'),
    path('contestar-mensaje/<pk>/', contestar_mensaje, name = 'contestar_mensaje'),
    path('eliminar-mensaje/<pk>/', eliminar_mensaje, name = 'eliminar_mensaje'),
    path('eliminar-conversacion/<pk>/', eliminar_conversacion, name = 'eliminar_conversacion'),
] 
