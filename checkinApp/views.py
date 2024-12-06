from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservaApp.models import Reserva  # Importar el modelo Reserva
from .forms import HuespedForm  # Importar el formulario HuespedForm

# Create your views here.

@login_required
def listado_checkin(request):
    # Permitir acceso si el usuario es superusuario o pertenece a los grupos admin o recepcion
    if request.user.is_superuser or request.user.groups.filter(name__in=['admin', 'recepcion']).exists():
        # Filtrar reservas con status 'R'
        reservas = Reserva.objects.filter(status='R')
        return render(request, 'checkinApp/listadoCheckin.html', {'reservas': reservas})
    else:
        # Mostrar un error 403 si no tiene permisos
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

# Vista para el formulario de Check In

def checkin_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    tipo_habitacion = reserva.tipoHab  # Obtenemos la categoría de la habitación asociada

    if request.method == 'POST':
        form = HuespedForm(request.POST)
        if form.is_valid():
            # Crear un nuevo huésped y asociarlo con la reserva
            huesped = form.save()
            
            # Verificar el estado de la reserva antes del Check-In
            if reserva.status == 'R':  # Solo modificamos si la reserva estaba activa
                # Aumentar la disponibilidad de la categoría (habitación vuelve a estar disponible)
                tipo_habitacion.cantidad += 1
                tipo_habitacion.save()

                # Actualizar el estado de la reserva a 'I' (Check-In realizado)
                reserva.status = 'I'
                reserva.save()
            
            # Mensaje de éxito
            messages.success(request, "Check-In realizado con éxito. La habitación ahora está disponible para nuevas reservas.")
            
            # Redirigir a la página de listado de Check-In
            return redirect('listadoCheckin')
    else:
        form = HuespedForm()

    return render(request, 'checkinApp/checkinFormulario.html', {'form': form, 'reserva': reserva})
