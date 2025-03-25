from django.contrib import admin
from .models import NotificacionPublicacion, NotificacionComentario, NotificacionSeguir, NotificacionRespuestaComentario, NotificacionMeGusta

# Register your models here.

@admin.register(NotificacionPublicacion)
class NotificacionPublicacionAdmin(admin.ModelAdmin):
    list_display = [
        'autor',
        'publicacion',
        'leida'
    ]
    ordering = ['leida']

@admin.register(NotificacionComentario)
class NotificacionComentarioAdmin(admin.ModelAdmin):
    list_display = [
        'destinatario',
        'leida'
    ]
    ordering = ['leida']

@admin.register(NotificacionSeguir)
class NotificacionSeguirAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'destinatario',
        'leida'
    ]
    ordering = ['leida']

@admin.register(NotificacionRespuestaComentario)
class NotificacionRespuestaComentarioAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'destinatario',
        'leida'
    ]
    ordering = ['leida']


@admin.register(NotificacionMeGusta)
class NotificacionMegusta(admin.ModelAdmin):
    list_display = [
        'usuario',
        'destinatario',
        'leida'
    ]
    ordering = ['leida']