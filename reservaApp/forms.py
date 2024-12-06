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
        'placeholder': 'Ingresar nombre del contacto'
    }))
    tipoHab = forms.ModelChoiceField(queryset=TipoHab.objects.all(), label='Categoría', widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    pax = forms.IntegerField(label='Número huéspedes', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'min': '1',
        'placeholder': 'Ingresar número de huéspedes'
    }))
    fono = forms.CharField(label='Teléfono', max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingresar teléfono de contacto'
    }))
    garantia = forms.CharField(label='Garantía', max_length=4, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '4 últimos dígitos de tarjeta'
    }))
    fecha_entrada = forms.DateField(label='Fecha Ingreso', widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingresar fecha de ingreso',
        'type': 'date'
    }))
    fecha_salida = forms.DateField(label='Fecha Salida', widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese fecha de salida',
        'type': 'date'
    }))
    nota = forms.CharField(label='Observaciones para la Reserva', required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Ingresar observaciones adicionales para la reserva (opcional)',
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