from rest_framework import serializers
from .models import Reserva, TipoHab
from django.utils import timezone
from datetime import datetime

class ReservaSerializer(serializers.ModelSerializer):
    fecha_entrada = serializers.DateField(default=timezone.now)  # Definir un valor predeterminado aquí
    fecha_salida = serializers.DateField()

    class Meta:
        model = Reserva
        fields = ['titular', 'pax', 'fono', 'garantia', 'fecha_entrada', 'fecha_salida', 'total', 'status', 'tipoHab', 'nota']
        read_only_fields = ['fecha_entrada', 'total', 'status']

    def validate_fecha_salida(self, value):
        # Convertir 'fecha_entrada' a tipo datetime.date si es una cadena
        fecha_entrada = self.initial_data.get('fecha_entrada', datetime.now().date())
        if isinstance(fecha_entrada, str):  # Si fecha_entrada es una cadena, convertirla
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()

        # Asegurarse de que la fecha de salida sea posterior a la de entrada
        if value <= fecha_entrada:
            raise serializers.ValidationError("La fecha de salida debe ser posterior a la fecha de entrada.")
        return value
    
    def validate(self, data):
        """
        Validación de lógica adicional: Comprobar disponibilidad de habitación.
        """
        tipo_habitacion = data.get('tipoHab')
        
        try:
            tipo_habitacion_obj = TipoHab.objects.get(id=tipo_habitacion.id)
        except TipoHab.DoesNotExist:
            raise serializers.ValidationError({"tipoHab": "Tipo de habitación no válido."})
        
        # Verificar si hay disponibilidad
        if tipo_habitacion_obj.cantidad <= 0:
            raise serializers.ValidationError({"tipoHab": "No hay disponibilidad para esta categoría de habitación."})
        
        return data
    
    def create(self, validated_data):
        fecha_salida = validated_data.get('fecha_salida')
        fecha_entrada = validated_data.get('fecha_entrada', datetime.now().date())  # Asignar la fecha de entrada si no se proporciona

        # Calcular el número de noches
        if isinstance(fecha_entrada, str):  # Si fecha_entrada es una cadena, convertirla
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()

        numero_noches = (fecha_salida - fecha_entrada).days

        # Obtener el tipo de habitación
        tipo_habitacion = validated_data['tipoHab']

        # Calcular el total de la reserva
        total = tipo_habitacion.tarifa * numero_noches

        # Crear la reserva
        reserva = Reserva.objects.create(
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            total=total,
            status="R",  # Estado 'R' para reserva confirmada
            **validated_data
        )

        # Reducir la cantidad de habitaciones disponibles
        tipo_habitacion.cantidad -= 1
        tipo_habitacion.save()

        return reserva
