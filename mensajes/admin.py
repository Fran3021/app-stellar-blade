from django.contrib import admin
from .models import Conversacion, Mensaje

@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = [
        'usuario1',
        'usuario2',
        'fecha_inicio',
        'pk',
    ]
    ordering = ['fecha_inicio']


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = [
        'conversacion',
        'autor',
        'destinatario',
        'leido'
    ]
    ordering = ['leido']