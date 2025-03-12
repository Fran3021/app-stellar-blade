from django.conf import settings
from .forms import ContestarComentarioForm

def formulario_contestar_comentario(request):
    return {
        'contestar_form': ContestarComentarioForm()
    }