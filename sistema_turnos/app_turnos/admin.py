from django.contrib import admin
from .models import Empleado, Cliente, Servicio, Turno

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'horario_inicio', 'horario_fin')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'email')

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display= ('nombre', 'duracion_minutos', 'precio')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'empleado', 'cliente', 'servicio', 'fecha_hora_inicio', 'fecha_hora_fin', 'estado', 'codigo_reserva')
    list_filter = ('estado', 'empleado', 'servicio')
    search_fields = ('cliente__nombre', 'codigo_reserva')
    readonly_fields = ('fecha_hora_fin', 'codigo_reserva')
