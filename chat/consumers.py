import httpx, json, mimetypes, base64, os, uuid

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Contacto, Mensaje, ContactoTarea, SectorTarea, ContactoIntegracion, MensajeAdjunto
from config import settings

from .whatsapp import enviar_mensaje_greenapi, enviar_mensaje_waapi, enviar_adjunto_waapi


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
        subestado = None
        media = data['media']

        #contacto = await sync_to_async(Contacto.objects.get)(id=contacto)
        
        if media:
            media = await self.guardar_media_servidor(media, contacto)
        
        if integracion == 'WhatsApp':
            response = None
            if media:
                response = await enviar_adjunto_waapi(chat_id=telefono, mensaje=mensaje, url_adjunto=media)
            else:
                response = await enviar_mensaje_waapi(chat_id=telefono, mensaje=mensaje)
            # Manejar cuando se envia una foto pero no la puede descargar el whatsapp:
            #{'data': {'status': 'error', 'message': 'failed to download media file', 'instanceId': '4238'}, 'links': {'self': 'https://waapi.app/api/v1/instances/4238/client/action/send-media'}, 'status': 'success'}
            print(response)
            estado = response['status']
            subestado = response['data']['status']  # Cuando la API no puede descargar el error el estado es 'success' pero el subestado es 'error' 
        elif integracion == 'Test':
            if ambiente == 'Homologacion':
                usuario = None
                # Llamar función chequear_si_se_activa_chatbot
            estado = 'success'
            subestado = 'success'

        if estado == 'success' and subestado == 'success':
            usuario = await self.save_message(usuario, contacto, mensaje, media)
            await self.channel_layer.group_send(
                'global',
                {
                    'type': 'chat_message',
                    'contacto': contacto,
                    'mensaje': mensaje,
                    'usuario': usuario,
                    'url_adjunto': media
                }
            )
        else:
            print('No se pudo enviar el mensaje')
            await self.channel_layer.group_send(
                'global',
                {
                    'type': 'message_error',
                    'contacto': contacto,
                    'mensaje': 'No se pudo enviar el mensaje. Por favor, recargue la página y vuelva a intentarlo',
                    'usuario': usuario,
                    'url_adjunto': media
                }
            )

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
            'usuario': event['usuario'],
            'url_adjunto': event['url_adjunto']
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

    async def message_error(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'contacto': event['contacto'],
            'mensaje': event['mensaje'],
            'usuario': event['usuario']
        }))

    @sync_to_async
    def guardar_media_servidor(self, media, contacto):
        try:
            mimetype, media64 = media.split(',', 1)
            mimetype = media.split(';', 1)[0].split(':', 1)[1]
            archivo64 = base64.b64decode(media64)
            extension = mimetypes.guess_extension(mimetype)
            nombre_archivo = f'{str(uuid.uuid4())}{extension}'
            url_relativa = os.path.join('adjuntos', str(contacto), nombre_archivo)
            url_absoluta = os.path.join(settings.MEDIA_ROOT, url_relativa)
            print(url_absoluta)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'adjuntos', str(contacto)), exist_ok=True)
            with open(url_absoluta, "wb") as f:
                f.write(archivo64)
            # Obtener el host del servidor
            headers = dict(self.scope['headers'])
            host = headers.get(b'origin', b'').decode('utf-8')
            url_adjunto = f'{host}/media/{url_relativa}'
            return url_adjunto
        except Exception as e:
            print(str(e))
            print('No se pudo guardar el archivo en el servidor')

    @sync_to_async
    def save_message(self, usuario, contacto, mensaje, url_adjunto):
        user = User.objects.filter(username=usuario)
        user = user.first() if user.exists() else None
        contacto = Contacto.objects.get(id=contacto)
        contacto_integracion = ContactoIntegracion.objects.get(contacto=contacto)
        mensaje = Mensaje.objects.create(usuario=user, contacto_integracion=contacto_integracion, contenido=mensaje)
        if url_adjunto:
            url_relativa = url_adjunto.split('/media/', 1)[1]
            MensajeAdjunto.objects.create(url=url_relativa, mensaje=mensaje)
        return user.username if user else contacto_integracion.contacto.nombre

    @sync_to_async
    def save_sector_change(self, contacto, sector_tarea):
        contacto_tarea = ContactoTarea.objects.filter(contacto_integracion_id=contacto).first()
        sector_tarea_destino = SectorTarea.objects.filter(id=sector_tarea).first()
        if contacto_tarea and sector_tarea_destino:
            contacto_tarea.sector_tarea = sector_tarea_destino
            contacto_tarea.save()

'''
{
    'type': 'websocket', 
    'path': '/ws/global/', 
    'raw_path': b'/ws/global/', 
    'headers': [
        (b'host', b'127.0.0.1:8000'), 
        (b'connection', b'Upgrade'), 
        (b'pragma', b'no-cache'), 
        (b'cache-control', b'no-cache'), 
        (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
        (b'upgrade', b'websocket'),
        (b'origin', b'http://127.0.0.1:8000'),
        (b'sec-websocket-version', b'13'),
        (b'accept-encoding', b'gzip, deflate, br'),
        (b'accept-language', b'en-US,en;q=0.9,es-AR;q=0.8,es;q=0.7'),
        (b'cookie', b'csrftoken=9UiKkQrw9UPI1PEg2U8ESwQjRuocOcNmmBHgm1DgLgJvvJCjNJXAmmlWPyJsfQ4f; sessionid=27l616z9lvc4j3t49wit90ip05hv4viw'),
        (b'sec-websocket-key', b'V87YhzukthhOuU+wQVui9g=='), (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')
    ],
    'query_string': b'',
    'client': ['127.0.0.1', 55213],
    'server': ['127.0.0.1', 8000],
    'subprotocols': [],
    'asgi': {'version': '3.0'},
    'cookies': {
        'csrftoken': '9UiKkQrw9UPI1PEg2U8ESwQjRuocOcNmmBHgm1DgLgJvvJCjNJXAmmlWPyJsfQ4f',
        'sessionid': '27l616z9lvc4j3t49wit90ip05hv4viw'
    },
    'session': <django.utils.functional.LazyObject object at 0x0000020C2AFD0280>,
    'user': <channels.auth.UserLazyObject object at 0x0000020C2AFD0880>,
    'path_remaining': '',
    'url_route': {
        'args': (), 'kwargs': {}
    }
}
'''