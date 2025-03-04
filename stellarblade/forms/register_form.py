from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget = forms.PasswordInput(), label= 'Escriba su contraseña')
    password2 = forms.CharField(widget = forms.PasswordInput(), label= 'Repita su contraseña su contraseña')
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
