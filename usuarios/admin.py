from django.contrib import admin
from.models import PerfilUsuario, Follow

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'fecha_nacimiento',
        'pk',
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'seguidor',
        'siguiendo',
        'fecha_inicio',
    ]
