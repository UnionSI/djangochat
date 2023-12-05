import json
import httpx

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message, ContactoTarea, SectorTarea


class GlobalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('global', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('global', self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'chat_message':
            # Procesar mensaje de chat
            message = data['message']
            username = data['username']
            room = data['room']
            phone = data['phone']

            # Guardar el mensaje en la base de datos
            await self.save_message(username, room, message)

            # Send whatsapp message
            await self.send_whatsapp_message(chat_id=phone, message=message)

            # Enviar mensaje global
            await self.channel_layer.group_send(
                'global',
                {
                    'type': 'chat_message',
                    'room': room,
                    'message': message,
                    'username': username
                }
            )

        elif message_type == 'sector_change':
            # Procesar cambio de sector
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

            # Guardar cambio en la base de datos
            await self.save_sector_change(contacto, sector_tarea)

            # Enviar mensaje global
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
            'room': event['room'],
            'message': event['message'],
            'username': event['username']
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
    def save_message(self, username, room, message):
        user = User.objects.filter(username=username)
        user = user.first() if user.exists() else None
        room = Room.objects.get(id=room)
        message = Message.objects.create(usuario=user, contacto=room, contenido=message)

    @sync_to_async
    def save_sector_change(self, contacto, sector_tarea):
        print(contacto)
        contacto_tarea = ContactoTarea.objects.filter(contacto_id=contacto).first()
        print(contacto_tarea)
        sector_tarea_destino = SectorTarea.objects.filter(id=sector_tarea).first()
        print(sector_tarea_destino)
        if contacto_tarea and sector_tarea_destino:
            contacto_tarea.sector_tarea = sector_tarea_destino
            contacto_tarea.save()

    async def send_whatsapp_message(self, chat_id, message):
        id_instance = "7103880835"
        api_token_instance = "89bddd8da48246f593916d55b8be98e059a136b7b7e6469291"

        url = f'https://api.greenapi.com/waInstance{id_instance}/sendMessage/{api_token_instance}'

        payload = {
            "chatId": f"{chat_id}@c.us",
            "message": message
        }

        headers = {
            'Content-Type': 'application/json'
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=json.dumps(payload), headers=headers)

        return response.json()