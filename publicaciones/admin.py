from django.contrib import admin
from .models import Publicacion, Comentario, RespuestaComentario

# Register your models here.

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = [
        'titulo',
        'autor',
        'fecha_publicacion',
        'pk',
    ]
    ordering = ['-fecha_publicacion']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = [
        'autor',
        'fecha_comentario',
        'pk',
    ]
    ordering = ['-fecha_comentario']


@admin.register(RespuestaComentario)
class RespuestaComentarioAdmin(admin.ModelAdmin):
    list_display = [
        'autor',
        'respuesta',
        'fecha_respuesta'
    ]
    ordering = ['-fecha_respuesta']