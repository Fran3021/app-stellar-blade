from django.contrib import admin
from .models import Notificacion

# Register your models here.

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = [
        'mensaje',
        'leida'
    ]
    ordering = ['leida']