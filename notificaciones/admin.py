from django.contrib import admin
from .models import NotificacionPublicacion, NotificacionComentario, NotificacionSeguir

# Register your models here.

@admin.register(NotificacionPublicacion)
class NotificacionPublicacionAdmin(admin.ModelAdmin):
    list_display = [
        'mensaje',
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