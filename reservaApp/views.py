from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reservaApp.models import *
from reservaApp.forms import *
from django.http import HttpResponse
from fpdf import FPDF
from io import BytesIO
from datetime import timedelta
from django.contrib.auth.models import Group
from .models import Reserva, TipoHab 

# Create your views here.

def home(request):
    return render(request, 'reservasApp/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Iniciar sesión
                return redirect('gestionReservas')  # Redirigir a la gestión de reservas
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()
        
    return render(request, 'reservasApp/login.html', {'form': form})

#@login_required
#def gestionReservas(request):
    return render(request, 'reservasApp/gestionReservas.html')

@login_required
def gestionReservas(request):
    # Verifica si el usuario pertenece al grupo "reservas"
    usuario_reservas = request.user.groups.filter(name='reservas').exists()
    
    # Pasa esta información al contexto para usarla en el template
    return render(request, 'reservasApp/gestionReservas.html', {'usuario_reservas': usuario_reservas})

@login_required
def listadoReservas(request):
    reservas = Reserva.objects.filter(status='R') # Solo reservas activas
    data = {'reservas': reservas}
    return render(request, 'reservasApp/listadoReservas.html', data)

def reservarHabitacion(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            tipo_habitacion = form.cleaned_data['tipoHab']
            
            # Verificar disponibilidad
            if tipo_habitacion.cantidad > 0:
                # Calcular el total
                reserva = form.save(commit=False)  # No guardamos aún, porque vamos a calcular el total

                # Obtener la tarifa de la habitación seleccionada
                tarifa = tipo_habitacion.tarifa

                # Calcular el total basado en las fechas
                fecha_entrada = reserva.fecha_entrada
                fecha_salida = reserva.fecha_salida
                numero_noches = (fecha_salida - fecha_entrada).days

                # Calcular el total
                total = tarifa * numero_noches
                reserva.total = total  # Asignamos el total calculado

                # Guardar la reserva con el total calculado
                reserva.save()

                # Restamos 1 a la cantidad de habitaciones disponibles
                tipo_habitacion.cantidad -= 1
                tipo_habitacion.save()  # Guardamos la nueva cantidad de habitaciones

                # Mensaje de éxito
                messages.success(request, "Reserva realizada con éxito.")
                
                # Redirigir según si el usuario está autenticado
                if request.user.is_authenticated:
                    # Usuario autenticado (probablemente admin o empleado) redirige a listado de reservas
                    return redirect('listadoReservas')  # Redirige al listado de reservas
                else:
                    # Usuario no autenticado (cliente) redirige a reserva exitosa
                    return render(request, "reservasApp/reservaExitosa.html", {"reserva": reserva})
            else:
                # Si no hay disponibilidad
                messages.error(request, "Lo sentimos, no hay disponibilidad para esta categoría.")
                return redirect('reservar')  # Redirigir al formulario con el mensaje de error
    else:
        form = ReservaForm()

    return render(request, "reservasApp/reservar.html", {"form": form})

@login_required
def actualizarReserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    tipo_habitacion_actual = reserva.tipoHab  # Tipo de habitación actual de la reserva
    form = ReservaForm(instance=reserva)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            tipo_habitacion_nueva = form.cleaned_data['tipoHab']  # Obtener el nuevo tipo de habitación
            
            # Mostrar detalles antes de la actualización para verificar
            print(f"Antes de la actualización: Tipo habitación actual ID: {tipo_habitacion_actual.id}, Tipo habitación nueva ID: {tipo_habitacion_nueva.id}")
            
            # Verificar si se cambia a un tipo de habitación diferente
            if tipo_habitacion_nueva.id != tipo_habitacion_actual.id:
                # Verificar disponibilidad de la nueva habitación
                if tipo_habitacion_nueva.cantidad > 0:
                    # Decrementar la cantidad de la nueva habitación
                    tipo_habitacion_nueva.cantidad -= 1  
                    tipo_habitacion_nueva.save()  # Guardar cambios en la nueva habitación

                    # Incrementar la cantidad de la habitación actual
                    tipo_habitacion_actual.cantidad += 1  
                    tipo_habitacion_actual.save()  # Guardar cambios en la habitación actual

                    messages.success(request, "La reserva se ha actualizado correctamente y se ha realizado el cambio de habitación.")
                else:
                    messages.error(request, "Lo siento, la nueva habitación seleccionada no está disponible.")
                    return redirect('actualizarReserva', reserva_id=reserva.id)  # Redirigir para corregir la elección

            # Calcular el total según las tarifas
            tarifa_nueva = tipo_habitacion_nueva.tarifa  # Asegúrate de tener un campo 'tarifa' en TipoHab
            dias_estancia = (reserva.fecha_salida - reserva.fecha_entrada).days
            total_nuevo = tarifa_nueva * dias_estancia
            
            reserva.tipoHab = tipo_habitacion_nueva
            reserva.total = total_nuevo  # Actualizar el total
            reserva.save()  # Guardar los cambios en la reserva
            
            messages.success(request, f"La reserva ha sido actualizada.")

            return redirect('listadoReservas')

    # Si el formulario no es válido, mostrar un mensaje de error
    if form.errors:
        messages.error(request, "Hubo un error al actualizar la reserva. Por favor, verifique los datos.")

    data = {'form': form, 'reserva': reserva}
    return render(request, 'reservasApp/editarReserva.html', data)

@login_required
def eliminarReserva(request, reserva_id):
    # Obtenemos la reserva utilizando el número de reserva
    reserva = get_object_or_404(Reserva, id=reserva_id)
    tipo_hab = reserva.tipoHab  # Recuperamos la categoría de la reserva

    if request.method == "POST":
        # Si el usuario confirma la eliminación, devolvemos la disponibilidad y eliminamos la reserva
        tipo_hab.cantidad += 1
        tipo_hab.save()  # Guardamos el cambio en la cantidad
        reserva.delete()
        
        # Mensaje de éxito
        messages.success(request, "Reserva eliminada con éxito.")
        
        return redirect('listadoReservas')
    
    # Si no es POST, simplemente redirigimos a listadoReservas con un mensaje de confirmación
    messages.warning(request, "¿Está seguro de eliminar esta reserva?")
    return redirect('listadoReservas')


@login_required
def listadoCategorias(request):
    categorias = TipoHab.objects.all()
    return render(request, 'reservasApp/listadoCategorias.html', {'categorias': categorias})

@login_required
def nuevaCategoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
            return redirect('listadoCategorias')  # Redirigir a la lista de categorías
    else:
        form = CategoriaForm()
    return render(request, 'reservasApp/nuevaCategoria.html', {'form': form})

def editarCategoria(request, categoria_id):
    categoria = TipoHab.objects.get(id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listadoCategorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'reservasApp/editarCategorias.html', {'form': form})

def eliminarCategoria(request, categoria_id):
    # Obtener la categoría a eliminar
    categoria = get_object_or_404(TipoHab, pk=categoria_id)

    # Verificar si hay reservas asociadas a esta categoría
    reservas = Reserva.objects.filter(tipoHab=categoria)

    if reservas.exists():
        # Si hay reservas, mostrar un mensaje de advertencia
        messages.error(request, 'No se puede eliminar la categoría porque existen reservas asociadas.')
        return redirect('listadoCategorias')  # Redirigir al listado de categorías

    # Si no hay reservas, proceder con la eliminación
    categoria.delete()
    messages.success(request, 'Categoría eliminada con éxito.')
    return redirect('listadoCategorias')  # Redirigir al listado de categorías

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def descargar_pdf(request, reserva_id):
    reserva = Reserva.objects.get(pk=reserva_id)

    # Crear una instancia de FPDF
    pdf = FPDF()
    pdf.add_page()

    # Encabezado con "ResOnlineApp" alineado a la derecha
    pdf.set_font("Arial", 'BI', size=12)
    pdf.cell(0, 10, 'ResOnlineApp', ln=True, align='L')
    pdf.cell(0, 10, '', ln=True)  # Espacio en blanco

    # Título en negrita
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Confirmación de Reserva", ln=True, align='C')
    
    # Regresar a la fuente normal para los campos
    pdf.set_font("Arial", size=12) 

    # Agregar contenido al PDF
    pdf.cell(200, 10, txt=f"N° Reserva: {reserva.id}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre Contacto: {reserva.titular}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo de Habitación: {reserva.tipoHab.nombre}", ln=True)
    pdf.cell(200, 10, txt=f"N° Huéspedes: {reserva.pax}", ln=True)
    pdf.cell(200, 10, txt=f"Fono Contacto: {reserva.fono}", ln=True)
    pdf.cell(200, 10, txt=f"Garantía: {reserva.garantia}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha de Entrada: {reserva.fecha_entrada.strftime('%d-%m-%Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha de Salida: {reserva.fecha_salida.strftime('%d-%m-%Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Total: ${reserva.total}", ln=True)
    pdf.cell(200, 10, txt=f"Nota: {reserva.nota}", ln=True)

    # Guardar el PDF en un objeto BytesIO
    from io import BytesIO
    pdf_output = BytesIO()
    pdf.output(dest='S')  # Generar el PDF en formato string (S)
    pdf_output.write(pdf.output(dest='S').encode('latin1'))  # Escribir el PDF en BytesIO

    # Crear la respuesta con el PDF
    response = HttpResponse(pdf_output.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reserva_{reserva_id}.pdf"'

    return response

