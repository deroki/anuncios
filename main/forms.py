from django import forms
from django.core.exceptions import ValidationError

from main import models
from main.models import Cliente
from dal import autocomplete


class ClienteForm(forms.ModelForm):
    usuario = forms.CharField(required=False,
                              widget=forms.HiddenInput())
    class Meta:
        model = models.Cliente
        fields = ('usuario','admin', 'color', 'logo')


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Logo
        fields = ('image',)


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'empresa', 'is_staff', 'is_cliente', 'is_montador')
        labels = {'first_name': 'Nombre',
                  'last_name': 'Apellidos',
                  'is_staff': 'Administrador',
                  'is_cliente': 'Cliente',
                  'is_montador': 'Montador',
                  'empresa': 'Empresa'}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# TODO quitar el campo usuario y hacer que user el usuario que hemos metido en el form despues del save de este
class MontadorForm(forms.ModelForm):
    class Meta:
        model = models.Montador
        fields = ['dni', 'ciudad', 'provincia','comunidad']


class CampanaForm(forms.ModelForm):
    pdvs = forms.CharField(required=False, widget=forms.HiddenInput())
    fecha_finalizado = forms.DateField(required=False, widget=forms.HiddenInput())
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(),
                                     required=False,
                                     widget=forms.HiddenInput())
    estado = forms.CharField(required=False, widget=forms.HiddenInput(),
                             initial='pendiente')
    class Meta:
        model = models.Campana
        fields = "__all__"

class PdvForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Si'),
        (False, 'No')
    )

    class Meta:
        model = models.Pdv
        fields = ['cliente', 'cadena', 'nombre', 'direccion', 'cp', 'ciudad', 'provincia', 'prioridad', 'activo', 'zona','permisos','observaciones', 'mail', 'telefono', 'persona_contacto' ]
        widgets = {'cliente': autocomplete.ModelSelect2Multiple(url='ClientesAutocomplete'),
                   'zona' : autocomplete.ModelSelect2(url='ZonasAutocomplete')}


class PdiForm(forms.ModelForm):
    class Meta:
        model = models.Pdi
        fields = '__all__'
        labels = {
            'altoTotal' : 'altoTotal (cm)',
            'anchoVista' : 'anchoVista (cm)',
            'anchoTotal' : 'anchoVista (cm)',
            'altoVista' : 'anchoVista (cm)'
            }
        widgets = {'pdv' : autocomplete.ModelSelect2(url='PdvAutocomplete')}

    def clean_instaladores(self):
        instaladores = self.cleaned_data['instaladores']
        if instaladores < 0 :
            raise ValidationError("El número de instaladores no puede ser negativo")
        return instaladores

class CreatividadForm(forms.ModelForm):
    class Meta:
        model = models.Creatividad
        fields = '__all__'
        widgets = { 'campana' : autocomplete.ModelSelect2(url='CampanasAutocomplete') }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = '__all__'
