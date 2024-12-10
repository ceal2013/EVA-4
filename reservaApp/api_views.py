from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reserva, TipoHab
from .serializers import ReservaSerializer, TipoHabSerializer
from datetime import datetime

class ReservaListCreateAPIView(APIView):
    """
    Listar todas las reservas o crear una nueva reserva.
    """
    def get(self, request):
        reservas = Reserva.objects.all()
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        tipo_hab = TipoHab.objects.get(id=data['tipoHab'])

        # Verificar disponibilidad
        if tipo_hab.cantidad < 1:
            return Response({'error': 'No hay disponibilidad para esta categoría de habitación.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular total según noches
        fecha_entrada = datetime.strptime(data['fecha_entrada'], "%Y-%m-%d")
        fecha_salida = datetime.strptime(data['fecha_salida'], "%Y-%m-%d")
        noches = (fecha_salida - fecha_entrada).days
        if noches < 1:
            return Response({'error': 'La fecha de salida debe ser posterior a la fecha de entrada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        total = noches * tipo_hab.tarifa

        # Crear reserva
        data['total'] = total
        serializer = ReservaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Reducir cantidad de habitaciones
            tipo_hab.cantidad -= 1
            tipo_hab.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservaDetailAPIView(APIView):
    """
    Obtener, actualizar o eliminar una reserva específica.
    """
    def get(self, request, pk):
        try:
            reserva = Reserva.objects.get(pk=pk)
            serializer = ReservaSerializer(reserva)
            return Response(serializer.data)
        except Reserva.DoesNotExist:
            return Response({'error': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            reserva = Reserva.objects.get(pk=pk)
            serializer = ReservaSerializer(reserva, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reserva.DoesNotExist:
            return Response({'error': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            reserva = Reserva.objects.get(pk=pk)
            reserva.delete()
            return Response({'message': 'Reserva eliminada con éxito'}, status=status.HTTP_204_NO_CONTENT)
        except Reserva.DoesNotExist:
            return Response({'error': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)
