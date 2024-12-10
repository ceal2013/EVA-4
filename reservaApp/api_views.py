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
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

@login_required(login_url='login')  # Redirige al login si no está autenticado
@user_passes_test(lambda u: u.is_superuser, login_url='login')  # Verifica que sea superusuario
def api_dashboard_view(request):
    reservas = Reserva.objects.filter(status='R').order_by('id')
    return render(request, 'reservasApp/api_dashboard.html', {'reservas': reservas})

class ReservaListCreateAPIView(LoginRequiredMixin, ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminUser]  # Solo superusuarios pueden acceder

    # Esto asegura que un usuario debe estar autenticado antes de acceder a la vista
    login_url = 'login'  # Si no está autenticado, lo redirige al login

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

class ReservaDetailAPIView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAdminUser]  # Solo superusuarios pueden acceder

    # Esto asegura que un usuario debe estar autenticado antes de acceder a la vista
    login_url = 'login'  # Si no está autenticado, lo redirige al login

    def perform_update(self, serializer):
        reserva = self.get_object()
        tipo_hab_nuevo = serializer.validated_data.get('tipoHab', reserva.tipoHab)
        fecha_entrada_nueva = serializer.validated_data.get('fecha_entrada', reserva.fecha_entrada)
        fecha_salida_nueva = serializer.validated_data.get('fecha_salida', reserva.fecha_salida)

        if tipo_hab_nuevo.cantidad < 1:
            raise serializers.ValidationError({'tipoHab': 'No hay disponibilidad para esta categoría de habitación.'})

        if fecha_entrada_nueva != reserva.fecha_entrada or fecha_salida_nueva != reserva.fecha_salida:
            noches = (fecha_salida_nueva - fecha_entrada_nueva).days
            if noches < 1:
                raise serializers.ValidationError({'fecha_salida': 'La fecha de salida debe ser posterior a la fecha de entrada.'})

        total = noches * tipo_hab_nuevo.tarifa
        reserva.total = total
        reserva.tipoHab.cantidad += 1
        tipo_hab_nuevo.cantidad -= 1
        tipo_hab_nuevo.save()
        
        serializer.save(total=total, tipoHab=tipo_hab_nuevo, fecha_entrada=fecha_entrada_nueva, fecha_salida=fecha_salida_nueva)
        reserva.tipoHab.save()

    def perform_destroy(self, instance):
        tipo_hab = instance.tipoHab
        tipo_hab.cantidad += 1
        tipo_hab.save()
        instance.delete()