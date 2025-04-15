from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from usuarios.models import PerfilUsuario


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(), label= 'Escriba su contraseña')
    password_confirm = forms.CharField(widget = forms.PasswordInput(), label= 'Repita su contraseña su contraseña')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm and password != '':
            self.add_error('password_confirm','Las contraseñas no coinciden')

        return cleaned_data

    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            PerfilUsuario.objects.create(usuario = user)
        
        return user
