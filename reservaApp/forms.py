from django import forms
from .models import TipoHab, Reserva
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['titular', 'tipoHab', 'pax', 'fono', 'garantia', 'fecha_entrada', 'fecha_salida', 'nota']
        
    titular = forms.CharField(label='Nombre Contacto', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el nombre del contacto'
    }))
    tipoHab = forms.ModelChoiceField(queryset=TipoHab.objects.all(), label='Categoría', widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    pax = forms.IntegerField(label='Número de huéspedes', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'min': '1',
        'placeholder': 'Ingrese el número de huéspedes'
    }))
    fono = forms.CharField(label='Teléfono', max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese su número de teléfono'
    }))
    garantia = forms.CharField(label='Garantía', max_length=4, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '4 últimos dígitos de su tarjeta'
    }))
    fecha_entrada = forms.DateField(label='Fecha de Ingreso', widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese la fecha de ingreso',
        'type': 'date'
    }))
    fecha_salida = forms.DateField(label='Fecha de Salida', widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese la fecha de salida',
        'type': 'date'
    }))
    nota = forms.CharField(label='Observaciones para su Reserva', required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese observaciones adicionales para su reserva (opcional)',
        'rows': 3  # Ajusta el tamaño del área de texto
    }))

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = TipoHab
        fields = ['tipo', 'nombre', 'tarifa', 'cantidad']
        labels = {
            'tipo': 'Sigla',
            'nombre': 'Nombre',
            'tarifa': 'Tarifa',
            'cantidad': 'Disponibilidad'
        }