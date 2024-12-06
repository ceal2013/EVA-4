from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Reserva, TipoHab
from .serializers import ReservaSerializer
from django.utils import timezone

# Vista para listar todas las reservas y crear una nueva
class ReservaListCreateView(generics.ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        tipo_habitacion_id = self.request.data.get('tipoHab')
        fecha_salida = self.request.data.get('fecha_salida')

        if not fecha_salida:
            return Response({"error": "El campo 'fecha_salida' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tipo_habitacion = TipoHab.objects.get(id=tipo_habitacion_id)
        except TipoHab.DoesNotExist:
            return Response({"error": "Tipo de habitación no válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar disponibilidad de la habitación
        if tipo_habitacion.cantidad <= 0:
            return Response({"error": "No hay disponibilidad para esta categoría de habitación."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener la fecha de entrada (hoy)
        fecha_entrada = timezone.now().date()

        # Validar el serializador, ya maneja la fecha de salida
        reserva = serializer.save(
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            status="R"  # Estado 'R' para reserva confirmada
        )

        # Reducir la cantidad de habitaciones disponibles
        tipo_habitacion.cantidad -= 1
        tipo_habitacion.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
# Vista para obtener, actualizar y eliminar una reserva por ID
class ReservaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Lógica para cuando se actualiza una reserva
        reserva = serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, instance):
        # Lógica para cuando se elimina una reserva
        instance.delete()
        return Response({"message": "Reserva eliminada con éxito."}, status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        # Manejamos excepciones para enviar mensajes personalizados
        response = super().handle_exception(exc)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            response.data = {"error": "Reserva no encontrada."}
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {"error": "Hubo un problema con los datos de la solicitud."}
        return response

