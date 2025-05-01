from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from usuarios.models import PerfilUsuario
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(), label= _('Escriba su contraseña'))
    password_confirm = forms.CharField(widget = forms.PasswordInput(), label= _('Repita su contraseña'))
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
        self.fields['email'].required = False#ponemos que el email no sea obligatorio

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm and password != '':
            self.add_error('password_confirm',_('Las contraseñas no coinciden'))

        return cleaned_data

    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])#encriptamoos la contraseña

        if commit:
            user.save()
            PerfilUsuario.objects.create(usuario = user)
        
        return user
