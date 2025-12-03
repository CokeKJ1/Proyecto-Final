from django.urls import path
from .import views

urlpatterns = [
    path('', views.reservar_turno, name='reservar_turno'),
    path('cancelar/', views.cancelar_turno, name='cancelar_turno'),
    path('agenda/', views.agenda_empleado, name='agenda_empleado'),
]