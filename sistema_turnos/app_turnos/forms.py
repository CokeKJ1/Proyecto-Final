from django import forms
from .models import Turno, Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email']
        widgets = {
            'nombre' : forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'apellido' : forms.TextInput(attrs={'placeholder': 'Tu apellido'}),
            'telefono' : forms.TextInput(attrs={'placeholder': 'Numero de contacto'}),
            'email' : forms.EmailInput(attrs={'placeholder': 'juanpepito@gmail.com'}),
        }
#Formulario principal de reserva
class TurnoReservaForm(forms.ModelForm):
    class Meta:
       model = Turno
       fields = ['empleado', 'servicio', 'fecha_hora_inicio']
       widgets = {
           'fecha_hora_inicio': forms.DateTimeInput(attrs={
               'type': 'datetime-local',
           }),
       }
#Formulario para cancelar un turno
class TurnoCancelacionForm(forms.Form):
    codigo_reserva = forms.CharField(
        max_length=32,
        label="Codigo de Reserva",
        widget=forms.TextInput(attrs={'placeholder': 'Referencia: SD1232'})
    )