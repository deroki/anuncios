from django import forms

from main.models import Cliente, Logo


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre', 'admin', 'color', 'logo')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ('image',)