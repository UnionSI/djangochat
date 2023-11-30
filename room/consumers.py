import json
import httpx

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message, ContactoTarea

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

        # Send whatsapp message
        await self.send_whatsapp_message(chat_id=room, message=message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        message = Message.objects.create(usuario=user, contacto=room, contenido=message)
        return message

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