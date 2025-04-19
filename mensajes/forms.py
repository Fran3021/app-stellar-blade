from django import forms
from .models import Mensaje

#formulario que crea nuevos mensajes
class CreateMensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = [
            'contenido',
        ]

#formulario para contestar mensajes
class ContestarMensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = [
            'contenido',
        ]