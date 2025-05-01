from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
    value = forms.CharField(label=_("Introduce la palabra a buscar"), max_length=150)