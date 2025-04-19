from django.conf import settings
from .models import PerfilUsuario

#procesador de usuario que este logeado actualmente en la pagina
def current_user(request):
    return {
        'current_user': request.user,
    }


#funcion para el template de usuarios sugeridos en base de si esta logeado o si el usuario logeado lo tiene en seguidores
def all_users(request):
    if request.user.is_authenticated:
        perfil_usuario = request.user.perfil
        all_users = PerfilUsuario.objects.all().exclude(usuario=request.user).exclude(pk__in=perfil_usuario.seguidores.all())
        return {
            'all_users': all_users
        }
    else:
        all_users = PerfilUsuario.objects.all()
        return {
            'all_users': all_users
        }