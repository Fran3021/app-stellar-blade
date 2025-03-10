from django.conf import settings
from .models import Notificacion

def notificaciones(request):
    notificaciones = Notificacion.objects.filter(destinatarios=request.user.perfil)
    return {
        'notificacion': notificaciones
    }