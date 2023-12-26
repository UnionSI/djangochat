from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.contrib.auth.models import User
from chat.models import Integracion, Room, Message, SectorTarea, ContactoTarea

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@csrf_exempt
def green_api_webhook(request):
    # WaApi
    # key: ETBu4KVOMXT2KCL1t9SGRIJ7Ra8zEPFM60QINdAp3GjD5Ba
    # XtkLU4toIS8PzXdZGjQIUFOUzhFzxxmcUqoVCRwUd46d9dc9
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        if data:
            idMessage = data['idMessage']
            instanceData = data['instanceData']['typeInstance']
            phoneNumberRaw = data['senderData']['sender']
            phoneNumber = phoneNumberRaw.split('@')[0]
            name = data['senderData']['chatName']
            contentMessage = data['messageData']['extendedTextMessageData']['text']
            timestamp = data['timestamp']

        #room = Room.objects.all().first()

        IntegracionWhatsApp = Integracion.objects.get(nombre=instanceData)

        if IntegracionWhatsApp:
            contacto = Room.objects.filter(telefono=phoneNumber).first()
            if contacto:
                Message.objects.create(contacto=contacto, contenido=contentMessage)
            else:
                contacto = Room.objects.create(
                    nombre = name,
                    apellido = name,
                    dni = phoneNumber[:9],
                    telefono = phoneNumber,
                    email = phoneNumberRaw,
                    empresa = name,
                    nro_socio = int(phoneNumber[:9]),
                    integracion = IntegracionWhatsApp,
                    slug = phoneNumber,
                )
                sector_chat_inicial = SectorTarea.objects.get(nombre='Chat inicial')
                ContactoTarea.objects.create(contacto=contacto, sector_tarea=sector_chat_inicial)
                Message.objects.create(contacto=contacto, contenido=contentMessage)
            
            ''' Verificar si se tiene que activar un bot si el msg esta en un sector de bot '''

            # Enviar mensaje al canal de WebSocket
            channel_layer = get_channel_layer()
            '''
            async_to_sync(channel_layer.group_send)(
                f'chat_{phoneNumber}',  # Asegúrate de que esta coincida con tu patrón de nombres de sala
                {
                    'type': 'chat.message',
                    'message': contentMessage,
                    'username': contacto.nombre
                }
            )
            '''
            async_to_sync(channel_layer.group_send)(
                'global',
                {
                    'type': 'chat_message',
                    'room': contacto.id,
                    'message': contentMessage,
                    'username': contacto.nombre
                }
            )

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

'''
{
	"receiptId": 1,
	"body": {
		"typeWebhook": "incomingMessageReceived",
		"instanceData": {
			"idInstance": 7103880835,
			"wid": "5491130274052@c.us",
			"typeInstance": "whatsapp"
		},
	"timestamp": 1701266546,
	"idMessage": "885F9D3D019F46885C",
	"senderData": {
			"chatId": "5491160130996@c.us",
			"chatName": "Gona",
			"sender": "5491160130996@c.us",
			"senderName": "Gona"
			},
	"messageData": {
			"typeMessage": "extendedTextMessage",
			"extendedTextMessageData": {
				"text": "holaa",
				"description": "",
				"title": "",
				"previewType": "None",
				"jpegThumbnail": "",
				"forwardingScore": 0,
				"isForwarded": false
			}
		}
	}
}
'''