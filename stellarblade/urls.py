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
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from .views import home_view, legal_view, logout_view, RegisterView, LoginView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home_view, name = 'home'),
    path('legal/', legal_view, name = 'legal'),
    path('logout/', logout_view, name = 'logout'),
    path('registro/', RegisterView.as_view(), name = 'registro'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('usuarios/', include('usuarios.urls', namespace = 'usuarios')),
    path('publicaciones/', include('publicaciones.urls', namespace = 'publicaciones')),
    path('admin/', admin.site.urls),
] + debug_toolbar_urls() + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
