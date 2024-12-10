"""
URL configuration for ReservasOnline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reservaApp import views, api_views
from reservaApp.api_views import ReservaListCreateAPIView, ReservaDetailAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('checkin/', include('checkinApp.urls')),  # Asegúrate de incluir las URLs de checkinApp
    path('gestionReservas/', views.gestionReservas, name='gestionReservas'),
    path('listadoReservas/', views.listadoReservas, name='listadoReservas'),
    path('editarReserva/<int:reserva_id>/', views.actualizarReserva, name='actualizarReserva'),
    path('eliminarReserva/<int:reserva_id>/', views.eliminarReserva, name='eliminarReserva'),
    path('reservar/', views.reservarHabitacion, name='reservar'),
    path('descargar_pdf/<int:reserva_id>/', views.descargar_pdf, name='descargar_pdf'),
    path('editarCategoria/<int:categoria_id>/', views.editarCategoria, name='editarCategoria'),
    path('listadoCategorias/', views.listadoCategorias, name='listadoCategorias'),
    path('nuevaCategoria/', views.nuevaCategoria, name='nuevaCategoria'),
    path('eliminarCategoria/<int:categoria_id>/', views.eliminarCategoria, name='eliminarCategoria'),

    # Rutas de la API
    path('api/dashboard/', api_views.api_dashboard_view, name='apiDashboard'),
    path('api/reservas/', ReservaListCreateAPIView.as_view(), name='api_reserva_list_create'),
    path('api/reservas/<int:pk>/', ReservaDetailAPIView.as_view(), name='api_reserva_detail'),

]
