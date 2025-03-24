from django import forms

class SearchForm(forms.Form):
    value = forms.CharField(label="Introduce la palabra a buscar", max_length=150)