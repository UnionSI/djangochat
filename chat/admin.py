from django.contrib import admin
from .models import Integracion, Sector, SectorTarea, Room, ContactoIntegracion, ContactoTarea, Message, MensajeAdjunto

@admin.register(Integracion)
class AdminIntegracion(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Sector)
class AdminSector(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(SectorTarea)
class AdminSectorTarea(admin.ModelAdmin):
    list_display = ('nombre', 'sector', 'activo')

@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(ContactoIntegracion)
class AdminContactoIntegracion(admin.ModelAdmin):
    list_display = ('contacto', 'integracion')

@admin.register(ContactoTarea)
class AdminContactoTarea(admin.ModelAdmin):
    list_display = ('contacto_integracion', 'sector_tarea', 'usuario', 'fecha_hora')

@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ('contacto_integracion', 'usuario', 'contenido', 'fecha_hora', 'recibido', 'leido', 'id_integracion')

@admin.register(MensajeAdjunto)
class AdminMensajeAdjunto(admin.ModelAdmin):
    list_display = ('url', 'mensaje')

    