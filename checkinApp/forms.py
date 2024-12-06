from django import forms
from .models import Huesped

class HuespedForm(forms.ModelForm):
    class Meta:
        model = Huesped
        fields = ['nombre', 'apellido', 'dni', 'direccion', 'ciudad', 'pais','telefono', 'email', 'sexo']
        
    nombre = forms.CharField(label='Nombre', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese nombre'
    }))
    apellido = forms.CharField(label='Apellido', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese apellido'
    }))
    dni = forms.CharField(label='DNI', max_length=16, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese DNI o Pasaporte'
    }))    
    direccion = forms.CharField(label='Dirección', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese dirección'
    }))
    ciudad = forms.CharField(label='Ciudad', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese su ciudad'
    }))
    pais = forms.CharField(label='País', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese su país'
    }))
    telefono = forms.IntegerField(label='Teléfono', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese su número de teléfono'
    }))
    email = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese su correo electrónico'
    }))
    sexo = forms.CharField(label='Genero', max_length=1, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese su sexo'
    }))

    