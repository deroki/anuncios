from django import forms

from main import models


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ('usuario','admin', 'color', 'logo')


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Logo
        fields = ('image',)


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'empresa', 'password', 'is_staff', 'is_cliente', 'is_montador')
        labels = {'first_name': 'Nombre',
                  'last_name': 'Apellidos',
                  'is_staff': 'Administrador',
                  'is_cliente': 'Cliente',
                  'is_montador': 'Montador',
                  'empresa': 'Empresa'}


# TODO quitar el campo usuario y hacer que user el usuario que hemos metido en el form despues del save de este
class MontadorForm(forms.ModelForm):
    class Meta:
        model = models.Montador
        fields = '__all__'