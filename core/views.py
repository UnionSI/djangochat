from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.contrib.auth.models import User
from room.models import Integracion, Room, Message, SectorTarea, ContactoTarea
from .forms import SignUpForm

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def frontpage(request):
    return render(request, 'core/frontpage.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})


@csrf_exempt
def green_api_webhook(request):
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
            contacto = Room.objects.filter(nombre=name).first()
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

            # Enviar mensaje al canal de WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                phoneNumber,
                {
                    'type': 'chat.message',
                    'message': contentMessage,
                    #'username': contactoNuevo.nombre
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