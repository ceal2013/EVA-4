from django.contrib import admin
from .models import Huesped

# Personalización del modelo Huesped
@admin.register(Huesped)
class HuespedAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'pais', 'telefono', 'email')  # Mostrar columnas específicas
    search_fields = ('nombre', 'apellido', 'dni', 'email')  # Habilitar búsqueda
    list_filter = ('pais', 'sexo')  # Filtros por país y género
    ordering = ('apellido', 'nombre')  # Ordenar por apellido y nombre

# Configuración general del sitio
admin.site.site_header = "Hotel New"
admin.site.site_title = "Panel de Administración - Hotel New"
admin.site.index_title = "Gestión del Hotel New"
