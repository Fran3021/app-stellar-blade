from django.conf import settings
from .forms import ContestarMensajeForm

#funcion que renderize el formulario para contestar mensajes privados
def formulario_contestar_mensaje(request):
    return {
        'contestar_mensaje': ContestarMensajeForm()
    }