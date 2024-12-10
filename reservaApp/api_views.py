from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Reserva, TipoHab
from .serializers import ReservaSerializer
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def api_dashboard_view(request):
    # Lógica para mostrar la interfaz de la API
    return render(request, 'api_dashboard.html')

class ReservaListCreateAPIView(ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminUser]  # Solo superusuarios pueden acceder

    def perform_create(self, serializer):
        # Obtener datos del formulario
        tipo_hab = serializer.validated_data['tipoHab']
        fecha_entrada = serializer.validated_data['fecha_entrada']
        fecha_salida = serializer.validated_data['fecha_salida']

        # Verificar disponibilidad
        if tipo_hab.cantidad < 1:
            raise serializers.ValidationError({'tipoHab': 'No hay disponibilidad para esta categoría de habitación.'})

        # Calcular total según noches
        noches = (fecha_salida - fecha_entrada).days
        if noches < 1:
            raise serializers.ValidationError({'fecha_salida': 'La fecha de salida debe ser posterior a la fecha de entrada.'})
        
        total = noches * tipo_hab.tarifa

        # Actualizar campos automáticos y guardar
        serializer.save(total=total, status='R')
        tipo_hab.cantidad -= 1
        tipo_hab.save()


class ReservaDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminUser]  # Solo superusuarios pueden acceder

    def perform_update(self, serializer):
        # Si es necesario, puedes validar y actualizar campos adicionales aquí
        serializer.save()
