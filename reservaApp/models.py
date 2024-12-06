from django.db import models
from datetime import date

# Create your models here.

class TipoHab(models.Model):
    tipo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=50)
    tarifa = models.IntegerField()
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tipo} - {self.nombre} - {self.tarifa}"

class Reserva(models.Model):
    titular = models.CharField(max_length=100)
    tipoHab = models.ForeignKey(TipoHab, on_delete=models.CASCADE)
    pax = models.PositiveIntegerField()
    fono = models.CharField(max_length=15)
    garantia = models.CharField(max_length=4)
    fecha_entrada = models.DateField(default=date.today)
    fecha_salida = models.DateField(default=date.today)
    status = models.CharField(max_length=1, choices=[('R', 'Reservado'), ('I', 'Ingresado')], default='R')
    total = models.IntegerField(blank=True, null=True)
    nota = models.TextField(blank=True, null=True)      # Nota adicional

    def __str__(self):
        return f"{self.titular} - {self.tipoHab} - {self.fecha_entrada} - {self.fecha_salida}"

    def save(self, *args, **kwargs):
        # Calcular la tarifa total según la tarifa de la habitación y las noches
        if self.fecha_entrada and self.fecha_salida:
            dias = (self.fecha_salida - self.fecha_entrada).days
            self.total = self.tipoHab.tarifa * dias
        super().save(*args, **kwargs)
