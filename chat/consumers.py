import httpx, json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message, ContactoTarea, SectorTarea, ContactoIntegracion

from .whatsapp import send_greenapi_message, send_waapi_message


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
            integracion = data['integracion']
            ambiente = data['ambiente']
            status = None

            # Send whatsapp message
            if integracion == 'WhatsApp':
                response = await send_waapi_message(chat_id=phone, message=message)
                print(response)
                status = response['status']
                # validar si responde un 200 antes de continuar
            elif ambiente == 'Homologacion':
                username = None
                status = 'success'

            if status == 'success':
                # Guardar el mensaje en la base de datos
                username = await self.save_message(username, room, message)

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
            else:
                print('No se pudo enviar el mensaje')

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
        contacto_integracion = ContactoIntegracion.objects.get(contacto=room)
        message = Message.objects.create(usuario=user, contacto_integracion=contacto_integracion, contenido=message)
        return user.username if user else contacto_integracion.contacto.nombre

    @sync_to_async
    def save_sector_change(self, contacto, sector_tarea):
        print(contacto)
        contacto_tarea = ContactoTarea.objects.filter(contacto_integracion_id=contacto).first()
        print(contacto_tarea)
        sector_tarea_destino = SectorTarea.objects.filter(id=sector_tarea).first()
        print(sector_tarea_destino)
        if contacto_tarea and sector_tarea_destino:
            contacto_tarea.sector_tarea = sector_tarea_destino
            contacto_tarea.save()
