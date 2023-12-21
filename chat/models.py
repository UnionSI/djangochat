from django.contrib.auth.models import User
from django.db import models

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Integracion(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre
    

class Sector(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class SectorTarea(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField()  # Para que no se pierda las asignadas a un mensaje anterior si sacan una tarea

    def __str__(self):
        return self.nombre


class Room(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=11)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    empresa = models.CharField(max_length=100)
    nro_socio = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre


class ContactoIntegracion(models.Model):
    contacto = models.ForeignKey(Room, related_name='contacto_integraciones', on_delete=models.CASCADE)
    integracion = models.ForeignKey(Integracion, on_delete=models.CASCADE)


class ContactoTarea(models.Model):
    #contacto = models.ForeignKey(Room, related_name='contacto_tarea', on_delete=models.CASCADE)
    contacto_integracion = models.ForeignKey(ContactoIntegracion, related_name='contacto_tareas', on_delete=models.CASCADE)
    sector_tarea = models.ForeignKey(SectorTarea, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    

class Message(models.Model):
    #contacto = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    contacto_integracion = models.ForeignKey(ContactoIntegracion, related_name='messages', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE, null=True)
    contenido = models.TextField()
    recibido = models.DateTimeField()  # Verificar con la API
    leido = models.DateTimeField()  # Verificar con la API
    fecha_hora = models.DateTimeField(auto_now_add=True)
    id_integracion = models.CharField(max_length=25)  # ID del mensaje de la integración para citarlo

    # sector_tarea = models.ForeignKey(SectorTarea, on_delete=models.CASCADE) # Eliminar
    # chat (Si se saca la cabecera sacar este campo)
    # bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    # adjunto = (archivo/s)

    class Meta:
        ordering = ('fecha_hora',)

    def __str__(self):
        return self.contenido


class MensajeAdjunto(models.Model):
    url = models.URLField(max_length=200)
    mensaje = models.ForeignKey(Message, on_delete=models.CASCADE)
