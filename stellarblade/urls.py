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
from django.urls import path, include, re_path
from .views import legal_view, logout_view, RegisterView, LoginView, HomeView, search_view, PersonalizarReseteoContraseña, info_del_juego, politica_legal
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns#tenemos que importar esto para que funcione la traduccion


urlpatterns = [#aqui metemos las que no queremos que sean traducibles
    path('i18n/', include('django.conf.urls.i18n')),#esto nos incluye la vista set_language,viene propia de django
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += i18n_patterns (
    path('', HomeView.as_view(), name = 'home'),
    path('informacion-stellar-blade/', info_del_juego, name = 'info_del_juego'),
    path('politica-legal/', politica_legal, name = 'politica_legal'),
    path('logout/', logout_view, name = 'logout'),
    path('search/', search_view, name = 'search'),
    path('registro/', RegisterView.as_view(), name = 'registro'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('usuarios/', include('usuarios.urls', namespace = 'usuarios')),
    path('publicaciones/', include('publicaciones.urls', namespace = 'publicaciones')),
    path('notificaciones/', include('notificaciones.urls', namespace = 'notificaciones')),
    path('mensajes/', include('mensajes.urls', namespace = 'mensajes')),
    path('password_reset/', PersonalizarReseteoContraseña.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('admin/', admin.site.urls),
)

#para que solo se pueda acceder a rosetta si esta instalada en el proyecto
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
