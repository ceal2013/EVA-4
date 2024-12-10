from rest_framework import serializers
from .models import Reserva, TipoHab

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'titular', 'tipoHab', 'pax', 'fono', 'garantia', 'fecha_entrada', 'fecha_salida', 'nota', 'status', 'total']
        read_only_fields = ['status', 'total']  # Estos campos no se incluirán en la entrada del usuario

class TipoHabSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoHab
        fields = '__all__'
