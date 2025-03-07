from django import forms
from .models import Publicacion, Comentario

class CreatePublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = [
            'titulo',
            'imagen',
            'contenido',
        ]


class CreateComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = [
            'texto',
        ]