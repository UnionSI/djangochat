from django.contrib import admin

from .models import Sector, SectorTarea, Integracion, Room, Message, ContactoTarea

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

@admin.register(ContactoTarea)
class AdminContactoTarea(admin.ModelAdmin):
    list_display = ('contacto', 'sector_tarea', 'usuario', 'fecha_hora')

@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ('contacto', 'usuario', 'contenido', 'fecha_hora')