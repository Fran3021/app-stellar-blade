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
from .views import CrearPublicacionView, DetailPublicacionView, UpdatePublicacionView, DeletePublicacionView


app_name = 'publicaciones'

urlpatterns = [
    path('crear/', CrearPublicacionView.as_view(), name = 'crear'),
    path('detalle/<pk>', DetailPublicacionView.as_view(), name = 'detalle'),
    path('editar/<pk>', UpdatePublicacionView.as_view(), name = 'editar'),
    path('eliminar/<pk>', DeletePublicacionView.as_view(), name = 'delete'),
] 
