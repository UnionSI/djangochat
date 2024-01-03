from django.contrib.auth.models import User
from django.db import models

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Integracion(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = 'Integraciones'
    

class Sector(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Sectores'


class SectorTarea(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField()  # Para que no se pierda las asignadas a un mensaje anterior si sacan una tarea

    def __str__(self):
        return f'{self.sector} - {self.nombre}'

    class Meta:
        verbose_name_plural = 'Sectores tareas'


class Contacto(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    apellido = models.CharField(max_length=100, null=True)
    dni = models.CharField(max_length=11, null=True)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(max_length=60, null=True)
    empresa = models.CharField(max_length=100, null=True)
    nro_socio = models.PositiveIntegerField(null=True)
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.dni})'


class ContactoIntegracion(models.Model):
    contacto = models.ForeignKey(Contacto, related_name='contacto_integraciones', on_delete=models.CASCADE)
    integracion = models.ForeignKey(Integracion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contacto}-{self.integracion}'
    
    class Meta:
        verbose_name_plural = 'Contactos integraciones'


class ContactoTarea(models.Model):
    #contacto = models.ForeignKey(Room, related_name='contacto_tarea', on_delete=models.CASCADE)
    contacto_integracion = models.ForeignKey(ContactoIntegracion, related_name='contacto_tareas', on_delete=models.CASCADE)
    sector_tarea = models.ForeignKey(SectorTarea, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.contacto_integracion}-{self.sector_tarea}'
    
    class Meta:
        verbose_name_plural = 'Contactos tareas'


class Mensaje(models.Model):
    #contacto = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    contacto_integracion = models.ForeignKey(ContactoIntegracion, related_name='mensajes', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='mensajes', on_delete=models.CASCADE, null=True)
    contenido = models.TextField()
    id_integracion = models.CharField(max_length=25, null=True, blank=True)  # ID del mensaje de la integración para citarlo
    recibido = models.DateTimeField(null=True)  # Verificar con la API
    leido = models.DateTimeField(null=True)  # Verificar con la API
    fecha_hora = models.DateTimeField(auto_now_add=True)
    # sector_tarea = models.ForeignKey(SectorTarea, on_delete=models.CASCADE) # Eliminar
    # chat (Si se saca la cabecera sacar este campo)
    # bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    # adjunto = (archivo/s)

    class Meta:
        ordering = ('fecha_hora',)
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return self.contenido


class MensajeAdjunto(models.Model):
    url = models.URLField(max_length=200)
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Mensajes adjuntos'
