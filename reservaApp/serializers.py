from rest_framework import serializers
from .models import Reserva, TipoHab

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class TipoHabSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoHab
        fields = '__all__'
