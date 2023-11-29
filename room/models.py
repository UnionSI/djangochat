from django.contrib.auth.models import User
from django.db import models


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
    activo = models.BooleanField()  # Para ver no se pierda las asignadas a un mensaje anterior si sacan una tarea

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
    integracion = models.ForeignKey(Integracion, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre
    

class Message(models.Model):
    contacto = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE, null=True)
    contenido = models.TextField()
    recibido = models.BooleanField(default=False)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    #sector_tarea = models.ForeignKey(SectorTarea, on_delete=models.CASCADE) # Eliminar
    # chat (Si se saca la cabecera sacar este campo)
    # bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    # adjunto = (archivo/s)

    class Meta:
        ordering = ('fecha_hora',)

    def __str__(self):
        return self.contenido


class ContactoTarea(models.Model):
    contacto = models.ForeignKey(Room, related_name='contacto_tarea', on_delete=models.CASCADE)
    sector_tarea = models.ForeignKey(SectorTarea, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)


class MensajeAdjunto(models.Model):
    url = models.URLField(max_length=200)
    mensaje = models.ForeignKey(Message, on_delete=models.CASCADE)


'''

* Usuario (Base Users)

* Perfil
id Usuario

* Usuario Sector
id Usuario
id Sector

'''

# cargar todos los contactos room
# entra un nuevo mensaje se crea el objeto mensaje
# busco roomtarea atraves de room y chatbot inicial
# si esta en cerrado pasa a inicial
# si no hay nada pasa a inicial
# si esta en otro sector tarea queda en el que está, sin generar ningun registro

#chat bot cerrado
#chat bot inicial