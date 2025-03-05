from django.conf import settings

#procesador de usuario que este logeado actualmente en la pagina
def current_user(request):
    return {
        'current_user': request.user,
    }