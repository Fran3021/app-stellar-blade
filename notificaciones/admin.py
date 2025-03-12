from django.contrib import admin
from .models import NotificacionPublicacion

# Register your models here.

@admin.register(NotificacionPublicacion)
class NotificacionPublicacionAdmin(admin.ModelAdmin):
    list_display = [
        'mensaje',
        'leida'
    ]
    ordering = ['leida']