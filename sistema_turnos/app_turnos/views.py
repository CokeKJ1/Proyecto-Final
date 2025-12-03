from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Turno, Empleado, Cliente
from .forms import TurnoReservaForm, TurnoCancelacionForm, ClienteForm

def reservar_turno(request):
    cliente_form = ClienteForm(request.POST or None)
    reserva_form = TurnoReservaForm(request.POST or None)

    if request.method == 'POST':
        if cliente_form.is_valid() and reserva_form.is_valid():
            #Creacion o obtencion del cliente
            cliente_data = cliente_form.cleaned_data
            cliente, created = Cliente.objects.get_or_create(
                email = cliente_data['email'],
                defaults=cliente_data
            )

            #Obtencion de datos del turno
            empleado = reserva_form.cleaned_data['empleado']
            servicio = reserva_form.cleaned_data['servicio']
            fecha_hora_inicio = reserva_form.cleaned_data['fecha_hora_inicio']
            
            duracion = timedelta(minutes=servicio.duracion_minutos)
            fecha_hora_fin = fecha_hora_inicio + duracion

            #Bloqueo de turnos solapados
            turnos_solapados = Turno.objects.filter(
                empleado=empleado,
                estado='RESERVADO',
                #Comprobacion si el nuevo turno se solapa con algun turno existente
                fecha_hora_inicio__lt=fecha_hora_fin,
                fecha_hora_fin__gt=fecha_hora_inicio
            ).exists()

            if turnos_solapados:
                messages.error(request, "Este horario se solapa con otro turno reservado del empleado.")
                return render(request, 'app_turnos/reservar.html', {
                    'cliente_form' : cliente_form,
                    'reserva_form': reserva_form,
                    'mensaje':'Error de Solapamiento'
                })
            
            #Bloqueo de horarios no disponibles 
            hora_inicio_turno = fecha_hora_inicio.time()
            hora_fin_turno = fecha_hora_fin.time()

            if not (empleado.horario_inicio <= hora_fin_turno and hora_fin_turno <= empleado.horario_fin):
                messages.error(request, f"El turno ({hora_inicio_turno.strftime('%H:%M')} A {hora_inicio_turno.strftime('%H:%M')}) esta afuera del horario de atencion de {empleado.nombre} ({empleado.horario_inicio.strftime('%H:%M')} a {empleado.horario_fin.strftime('%H:%M')})")
                return render(request, 'app_turnos/reservar.html',{
                    'cliente_form' : cliente_form,
                    'reserva_form': reserva_form,
                    'mensaje':'Error de Horario'
                })
            
            turno = reserva_form.save(commit=False)
            turno.cliente = cliente
            turno.save()

            messages.success(request, f"!Turno reservado con exito! Codigo : {turno.codigo_reserva}")
            return redirect('reservar_turno')
    return render(request, 'app_turnos/reservar.html',{
        'cliente_form': cliente_form,
        'reserva_form': reserva_form,
        'mensaje': 'Reserva tu Turno'
    })
#Cancelar Turno
def cancelar_turno(request):
    cancelacion_form = TurnoCancelacionForm(request.POST or None)
    mensaje = "Ingresa el codigo para cancelar tu reserva."

    if request.method == 'POST' and cancelacion_form.is_valid():
        codigo = cancelacion_form.cleaned_data['codigo_reserva'].upper()
        
        try:
            turno = Turno.objects.get(codigo_reserva=codigo, estado='RESERVADO')
            turno.estado = 'CANCELADO'
            turno.save()

            messages.success(request, f"El turno (Codigo: {codigo}) ha sido cancelado con exito")
            return redirect('reservar_turno')
        
        except Turno.DoesNotExist:
            messages.error(request, f"No se encontro un turno RESERVADO con el codigo: {codigo}.")
    
    return render(request, 'app_turnos/cancelar.html',{
        'form': cancelacion_form,
        'mensaje': mensaje
    })

def agenda_empleado(request):
    empleados = Empleado.objects.all()
    agenda = []
    empleado_seleccionado = None

    empleado_id = request.GET.get('empleado.id')
    if empleado_id:
        try:
            empleado_seleccionado = get_object_or_404(Empleado, id=empleado_id)
            agenda = Turno.objects.filter(
                empleadp=empleado_seleccionado,
                estado__in=['RESERVADO'],
                fecha_hora_inicio__gte=datetime.now()
            ).order_by('fecha_hora_inicio')
        
        except Exception as e:
            messages.error(request, f"Error al cargar la agenda: {e}")
    return render(request, 'app_turnos/agenda.html',{
        'empleados': empleados,
        'agenda': agenda,
        'empleado_seleccionado': empleado_seleccionado,
        'mensaje': 'Agenda de Turnos'
    })
