from django.contrib import admin
from .models import Integracion, Sector, SectorTarea, Contacto, ContactoIntegracion, ContactoTarea, Mensaje, MensajeAdjunto

@admin.register(Integracion)
class AdminIntegracion(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Sector)
class AdminSector(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(SectorTarea)
class AdminSectorTarea(admin.ModelAdmin):
    list_display = ('nombre', 'sector', 'activo', 'orden')

@admin.register(Contacto)
class AdminContacto(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'telefono', 'email', 'nro_socio')
    search_fields = ('nombre', 'apellido', 'dni', 'telefono', 'email', 'nro_socio')
    ordering = ('dni',)

@admin.register(ContactoIntegracion)
class AdminContactoIntegracion(admin.ModelAdmin):
    list_display = ('contacto', 'integracion')

@admin.register(ContactoTarea)
class AdminContactoTarea(admin.ModelAdmin):
    list_display = ('contacto_integracion', 'sector_tarea', 'usuario', 'fecha_hora')

@admin.register(Mensaje)
class AdminMensaje(admin.ModelAdmin):
    list_display = ('contacto_integracion', 'usuario', 'contenido', 'mensaje_citado', 'fecha_hora', 'recibido', 'leido', 'id_integracion', 'mostrar_mensaje_adjunto')
    list_filter = ('contacto_integracion', 'usuario', 'fecha_hora', 'id_integracion')
    search_fields = ('contacto_integracion__contacto__nombre', 'contacto_integracion__contacto__apellido', 'usuario')


    def mostrar_mensaje_adjunto(self, obj):
        # Obtener el primer mensaje adjunto asociado a este mensaje
        primer_adjunto = obj.mensajes_adjuntos.first()
        # Mostrar el nombre del archivo si hay un adjunto, de lo contrario, mostrar None
        return primer_adjunto.archivo.name if primer_adjunto else None

    mostrar_mensaje_adjunto.short_description = 'Mensaje Adjunto'

@admin.register(MensajeAdjunto)
class AdminMensajeAdjunto(admin.ModelAdmin):
    #list_display = ('url', 'mensaje')
    list_display = ('archivo', 'formato', 'mensaje')
    list_filter = ('formato',)


    