from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from .models import Reserva, TipoHab
from .serializers import ReservaSerializer
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def api_dashboard_view(request):
    # Lógica para mostrar la interfaz de la API
    reservas = Reserva.objects.filter(status='R').order_by('id')
    return render(request, 'reservasApp/api_dashboard.html', {'reservas': reservas})

class ReservaListCreateAPIView(ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminUser]  # Solo superusuarios pueden acceder

    def perform_create(self, serializer):
        tipo_hab = serializer.validated_data['tipoHab']
        fecha_entrada = serializer.validated_data['fecha_entrada']
        fecha_salida = serializer.validated_data['fecha_salida']

        if tipo_hab.cantidad < 1:
            raise serializers.ValidationError({'tipoHab': 'No hay disponibilidad para esta categoría de habitación.'})

        noches = (fecha_salida - fecha_entrada).days
        if noches < 1:
            raise serializers.ValidationError({'fecha_salida': 'La fecha de salida debe ser posterior a la fecha de entrada.'})

        total = noches * tipo_hab.tarifa
    
        # Guarda la reserva
        reserva = serializer.save(total=total, status='R')
        tipo_hab.cantidad -= 1
        tipo_hab.save()


class ReservaDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminUser]  # Solo superusuarios pueden acceder

    def perform_update(self, serializer):
        # Si es necesario, puedes validar y actualizar campos adicionales aquí
        serializer.save()

    def perform_destroy(self, instance):
        # Obtener el tipo de habitación asociada a la reserva eliminada
        tipo_hab = instance.tipoHab
        
        # Incrementar la cantidad de habitaciones disponibles en TipoHab
        tipo_hab.cantidad += 1
        tipo_hab.save()

        # Eliminar la reserva
        instance.delete()
