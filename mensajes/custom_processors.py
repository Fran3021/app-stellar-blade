from django.conf import settings
from .forms import ContestarMensajeForm


def formulario_contestar_mensaje(request):
    return {
        'contestar_mensaje': ContestarMensajeForm()
    }