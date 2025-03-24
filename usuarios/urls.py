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
from .views import MyPerfilView, UpdatePerfilView, DeletePerfilView,PublicacionesMisContactosView, follow_perfiles_ajax, PerfilesDetailView

app_name = 'usuarios'

urlpatterns = [
    path('mi-perfil/<pk>/', MyPerfilView.as_view(), name = 'mi_perfil'),
    path('update-perfil/<pk>/', UpdatePerfilView.as_view(), name = 'update'),
    path('delete-perfil/<pk>/',DeletePerfilView.as_view() , name = 'delete'),
    path('publicaciones-mis-contactos/',PublicacionesMisContactosView.as_view() , name = 'mis_contactos'),
    path('follow/<pk>',follow_perfiles_ajax , name = 'follow'),
    path('perfiles-detail/<pk>',PerfilesDetailView.as_view() , name = 'detail'),
] 
