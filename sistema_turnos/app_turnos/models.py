from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

# Create your models here.

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    horario_inicio = models.TimeField(default='09:00:00')
    horario_fin = models.TimeField(default='18:00:00')

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank = True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    duracion_minutos = models.PositiveIntegerField(
        default=30,
        help_text="Duracion estimada del servicio en minutos."
    )
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.nombre} {self.duracion_minutos} min'

class Turno(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='turnos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)

    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(null=True, blank=True, editable=False)

    ESTADOS = [
        ('RESERVADO', 'Reservado'),
        ('CANCELADO', 'Cancelado'),
        ('COMPLETADO', 'Completado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='RESERVADO')

    codigo_reserva = models.CharField(max_length=32, unique=True, editable=False)

    def save(self, *args, **kwargs):
        duracion = timedelta(minutes=self.servicio.duracion_minutos)
        self.fecha_hora_fin = self.fecha_hora_inicio + duracion

        if not self.codigo_reserva:
            import uuid
            self.codigo_reserva = uuid.uuid4().hex[:8].upper()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Turno {self.id} - {self.cliente} con {self.empleado} el {self.fecha_hora_inicio.strftime("%d/%m %H:%M")}'
    
    class Meta:
        ordering = ['fecha_hora_inicio']
        verbose_name_plural = 'Turnos'