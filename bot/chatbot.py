from chat.models import Mensaje, SectorTarea, ContactoTarea
from django.contrib.auth.models import User
from usuario.models import Usuario

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async


@sync_to_async
def logica_chatbot(contacto_integracion, mensaje_recibido):
    contacto_tarea = ContactoTarea.objects.filter(contacto_integracion=contacto_integracion).first()
    #sector_chatbot = Sector.objects.get(name='Chatbot')
    tarea_sector_chatbot_inicial = SectorTarea.objects.get(nombre='Chatbot inicial')
    tarea_sector_finalizado = SectorTarea.objects.get(nombre='Finalizado')
    conversacion_nueva = True if contacto_tarea.sector_tarea == tarea_sector_finalizado else False
    if contacto_tarea.sector_tarea == tarea_sector_finalizado or contacto_tarea.sector_tarea == tarea_sector_chatbot_inicial:
        responde_chatbot(conversacion_nueva, contacto_integracion, mensaje_recibido, contacto_tarea)


def responde_chatbot(conversacion_nueva, contacto_integracion, mensaje_recibido, contacto_tarea):
    # Manejar respuesta del socio
    mensaje_a_enviar = ''
    if conversacion_nueva:
        mensaje_a_enviar = '¡Hola! Te doy la bienvenida 👋\nSoy tu asistente virtual de Mutual Agropecuaria.\n\n❌NO atendemos llamados ni audios\n✅ÚNICAMENTE mensajes por escrito\n\n¡Muchas gracias!'
        mover_contacto_de_sector_tarea(contacto_tarea, 'Chatbot inicial')
    else:
        if str(mensaje_recibido) == '1':
            mensaje_a_enviar = 'Opción aceptada. Lo cambiaremos al sector tarea "Contacto inicial" del sector CAC'
            mover_contacto_de_sector_tarea(contacto_tarea, 'Contacto inicial')
        else:
            mensaje_a_enviar = 'No entiendo su respuesta. Por favor, conteste solamente con las opciones indicadas'
    
    # Guardar mensaje en la base de datos
    usuario_chatbot = Usuario.objects.get(username='Chatbot')
    Mensaje.objects.create(contacto_integracion=contacto_integracion, usuario=usuario_chatbot, contenido=mensaje_a_enviar)

    try:
        channel_layer = get_channel_layer()
        #async_to_sync(channel_layer.group_send)(
        async_to_sync(channel_layer.group_send)(
            'global',
            {
                'type': 'chat_message',
                'contacto': contacto_integracion.id,
                'mensaje': mensaje_a_enviar,
                'usuario': usuario_chatbot.username,
                'url_adjunto': ''
            }
        )
    except Exception as e:
        # Manejar el error de manera apropiada (por ejemplo, imprimir el error)
        print(f"Error al enviar mensaje a través de WebSocket: {e}")


def mover_contacto_de_sector_tarea(contacto_tarea, sector_tarea_destino):
    sector_tarea_destino = SectorTarea.objects.get(nombre=sector_tarea_destino)
    contacto_tarea.sector_tarea = sector_tarea_destino
    contacto_tarea.save()