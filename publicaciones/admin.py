from django.contrib import admin
from .models import Publicacion, Comentario

# Register your models here.

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = [
        'titulo',
        'autor',
        'fecha_publicacion'
    ]
    ordering = ['-fecha_publicacion']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = [
        'autor',
        'fecha_comentario'
    ]
    ordering = ['-fecha_comentario']