from django import forms
from .models import Publicacion, Comentario, RespuestaComentario

#formulario para editar una publicacion
class CreatePublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = [
            'titulo',
            'imagen',
            'video',
            'contenido',
        ]


#formulario para crear comentario en publicacion
class CreateComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = [
            'texto',
        ]

#formulario para contestar comentario de una publicacion
class ContestarComentarioForm(forms.ModelForm):
    class Meta:
        model = RespuestaComentario
        fields = [
            'respuesta',
        ]