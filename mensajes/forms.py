from django import forms
from .models import Mensaje

class CreateMensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = [
            'contenido',
        ]

class ContestarMensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = [
            'contenido',
        ]