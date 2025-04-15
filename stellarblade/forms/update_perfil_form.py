from django import forms
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario



class PerfilUsuarioForm(forms.ModelForm):
    email = forms.EmailField(required=False, label='Email (opcional)')

    class Meta:
        model = PerfilUsuario
        fields = [
            'imagen_perfil',
            'biografia',
            'fecha_nacimiento',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        if commit:
            perfil.save()
            if self.user:
                self.user.email = self.cleaned_data['email']
                self.user.save()
        return perfil