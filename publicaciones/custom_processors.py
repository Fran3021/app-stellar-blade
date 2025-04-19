from django.conf import settings
from .forms import ContestarComentarioForm
from .models import Publicacion

#funcion para usar el formulario de contestar comentario
def formulario_contestar_comentario(request):
    return {
        'contestar_form': ContestarComentarioForm()
    }


#funcion para mostrar en la home todas la publicaciones, segun el usuario este logeado o no
def all_publicaciones(request):
    if request.user.is_authenticated:
        all_publicaciones = Publicacion.objects.all().exclude(autor=request.user.perfil)
        return {
            'all_publicaciones': all_publicaciones
        }
    else:
        all_publicaciones = Publicacion.objects.all()
        return {
            'all_publicaciones': all_publicaciones
        }