from django import forms
from .models import Publicacion

class CreatePublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = [
            'titulo',
            'imagen',
            'contenido',
        ]