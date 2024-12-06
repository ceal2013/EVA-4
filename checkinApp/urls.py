# checkinApp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('listado_checkin/', views.listado_checkin, name='listadoCheckin'),  # Listado de reservas pendientes
    path('checkin_reserva/<int:reserva_id>/', views.checkin_reserva, name='checkinReserva'),  # Formulario de Check In
]

