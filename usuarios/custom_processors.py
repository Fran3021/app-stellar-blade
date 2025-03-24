from django.conf import settings
from .models import PerfilUsuario

#procesador de usuario que este logeado actualmente en la pagina
def current_user(request):
    return {
        'current_user': request.user,
    }

def all_users(request):
    if request.user.is_authenticated:
        all_users = PerfilUsuario.objects.all().exclude(usuario=request.user)
        return {
            'all_users': all_users
        }
    else:
        all_users = PerfilUsuario.objects.all()
        return {
            'all_users': all_users
        }