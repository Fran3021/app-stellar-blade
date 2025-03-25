from django.conf import settings
from .forms import ContestarComentarioForm
from .models import Publicacion
def formulario_contestar_comentario(request):
    return {
        'contestar_form': ContestarComentarioForm()
    }

def all_publicaciones(request):
    if request.user.is_authenticated:
        all_publicaciones = Publicacion.objects.all().exclude(autor=request.user.perfil)
        return {
            'all_publicaciones': all_publicaciones
        }
    else:
        publicaciones = Publicacion.objects.all()
        return {
            'all_publicaciones': all_publicaciones
        }