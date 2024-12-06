from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from .models import Reserva, TipoHab
from checkinApp.models import Huesped

# Personalización del admin para Reservas
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('titular', 'tipoHab', 'fecha_entrada', 'fecha_salida', 'status', 'total')
    search_fields = ('titular', 'tipoHab__nombre')
    list_filter = ('status', 'tipoHab')
    date_hierarchy = 'fecha_entrada'
    ordering = ('fecha_entrada',)

# Personalización del admin para TipoHab
@admin.register(TipoHab)
class TipoHabAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad', 'tarifa')
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo',)

# Personalización del admin para User (usuarios)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')  # Se agrega 'get_groups'
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email')

    # Mostrar grupos como un campo adicional
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupos'  # Título de la columna en el admin


# Reemplaza el admin predeterminado de User con el personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Encabezados del sitio
admin.site.site_header = "Hotel New"
admin.site.site_title = "Panel de Administración - Hotel New"
admin.site.index_title = "Gestión del Hotel New"


