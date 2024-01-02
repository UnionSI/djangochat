import httpx, json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Contacto, Mensaje, ContactoTarea, SectorTarea, ContactoIntegracion

from .whatsapp import enviar_mensaje_greenapi, enviar_mensaje_waapi


class GlobalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('global', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('global', self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        tipo_mensaje = data['type']
        if tipo_mensaje == 'chat_message':
            await self.procesar_mensaje_chat(data)
        elif tipo_mensaje == 'sector_change':
            await self.procesar_cambio_de_sector(data)

    async def procesar_mensaje_chat(self, data):
        mensaje = data['mensaje']
        usuario = data['usuario']
        contacto = data['contacto']
        telefono = data['telefono']
        integracion = data['integracion']
        ambiente = data['ambiente']
        estado = None

        if integracion == 'WhatsApp':
            response = await enviar_mensaje_waapi(chat_id=telefono, message=mensaje)
            print(response)
            # Validar si responde un 200 antes de continuar
        elif integracion == 'Test':
            if ambiente == 'Homologacion':
                usuario = None
                # Llamar función chequear_si_se_activa_chatbot
            estado = 'success'

        if estado == 'success':
            usuario = await self.save_message(usuario, contacto, mensaje)
            await self.channel_layer.group_send(
                'global',
                {
                    'type': 'chat_message',
                    'contacto': contacto,
                    'mensaje': mensaje,
                    'usuario': usuario
                }
            )
        else:
            print('No se pudo enviar el mensaje')

    async def procesar_cambio_de_sector(self, data):
        sector = data['sector']
        sector_tarea = data['sector_tarea']
        contacto = data['contacto']
        slug = data['slug']
        no_leido = data['no_leido']
        thumbnail = data['thumbnail']
        cabecera = data['cabecera']
        dni = data['dni']
        usuario = data['usuario']
        mensaje = data['mensaje']
        fecha = data['fecha']

        await self.save_sector_change(contacto, sector_tarea)

        await self.channel_layer.group_send(
            'global',
            {
                'type': 'sector_change',
                'sector': sector,
                'sector_tarea': sector_tarea,
                'contacto': contacto,
                'slug': slug,
                'no_leido': no_leido,
                'thumbnail': thumbnail,
                'cabecera': cabecera,
                'dni': dni,
                'usuario': usuario,
                'mensaje': mensaje,
                'fecha': fecha,
            }
        )

    async def chat_message(self, event):
        # Enviar mensaje global a la conexión WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'contacto': event['contacto'],
            'mensaje': event['mensaje'],
            'usuario': event['usuario']
        }))

    async def sector_change(self, event):
        # Enviar mensaje global a la conexión WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'sector': event['sector'],
            'sector_tarea': event['sector_tarea'],
            'contacto': event['contacto'],
            'slug': event['slug'],
            'no_leido': event['no_leido'],
            'thumbnail': event['thumbnail'],
            'cabecera': event['cabecera'],
            'dni': event['dni'],
            'usuario': event['usuario'],
            'mensaje': event['mensaje'],
            'fecha': event['fecha'],
        }))


    @sync_to_async
    def save_message(self, usuario, contacto, mensaje):
        user = User.objects.filter(username=usuario)
        user = user.first() if user.exists() else None
        contacto = Contacto.objects.get(id=contacto)
        contacto_integracion = ContactoIntegracion.objects.get(contacto=contacto)
        mensaje = Mensaje.objects.create(usuario=user, contacto_integracion=contacto_integracion, contenido=mensaje)
        return user.username if user else contacto_integracion.contacto.nombre

    @sync_to_async
    def save_sector_change(self, contacto, sector_tarea):
        contacto_tarea = ContactoTarea.objects.filter(contacto_integracion_id=contacto).first()
        sector_tarea_destino = SectorTarea.objects.filter(id=sector_tarea).first()
        if contacto_tarea and sector_tarea_destino:
            contacto_tarea.sector_tarea = sector_tarea_destino
            contacto_tarea.save()
