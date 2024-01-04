from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.contrib.auth.models import User
from chat.models import Integracion, Contacto, Mensaje, SectorTarea, ContactoTarea, ContactoIntegracion

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

        IntegracionWhatsApp = Integracion.objects.get(nombre=instanceData)

        if IntegracionWhatsApp:
            contacto = Contacto.objects.filter(telefono=phoneNumber).first()
            if contacto:
                Mensaje.objects.create(contacto=contacto, contenido=contentMessage)
            else:
                contacto = Contacto.objects.create(
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
                Mensaje.objects.create(contacto=contacto, contenido=contentMessage)
            
            ''' Verificar si se tiene que activar un bot si el msg esta en un sector de bot '''

            # Enviar mensaje al canal de WebSocket
            channel_layer = get_channel_layer()
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
  
  
@csrf_exempt
def waapi_api_webhook(request):
    print('Consultando webhook waapi_api_webhook')
    print(request)
    print(request.method)
    if request.method == 'POST':
        print('entró al POST')
        data = json.loads(request.body.decode('utf-8'))
        print(f'\n***\n{data}\n***\n')
        if data:
            evento = data['event']
            instancia_id = data['data']['instanceId']
            mensaje_id = data['data']['message']['id']['id']
            contenido_mensaje = data['data']['message']['body']
            telefono_crudo = data['data']['message']['from']
            telefono = telefono_crudo.split('@')[0]
            nombre = data['data']['message']['_data']['notifyName']
            timestamp = data['data']['message']['timestamp']

        integracion_whatsapp = Integracion.objects.get(nombre='WhatsApp')

        if integracion_whatsapp:
            contacto = Contacto.objects.filter(telefono=telefono).first()
            if contacto:
                contacto_integracion = ContactoIntegracion.objects.get(contacto=contacto)
                Mensaje.objects.create(contacto_integracion=contacto_integracion, contenido=contenido_mensaje, id_integracion=mensaje_id)
            else:
                contacto = Contacto.objects.create(telefono = telefono)
                contacto_integracion = ContactoIntegracion.objects.create(contacto=contacto, integracion=integracion_whatsapp)
                sector_chat_inicial = SectorTarea.objects.get(nombre='Chat inicial')
                ContactoTarea.objects.create(contacto_integracion=contacto_integracion, sector_tarea=sector_chat_inicial)
                Mensaje.objects.create(contacto_integracion=contacto_integracion, contenido=contenido_mensaje, id_integracion=mensaje_id)            
            
            ''' Verificar si se tiene que activar un bot si el msg esta en un sector de bot '''

            # Enviar mensaje al canal de WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'global',
                {
                    'type': 'chat_message',
                    'contacto': contacto_integracion.id,
                    'mensaje': contenido_mensaje,
                    'usuario': contacto.nombre if contacto.nombre else contacto.telefono
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

'''
{
  "data": {
    "status": "success",
    "instanceId": "4107",
    "data": {
      "_data": {
        "id": {
          "fromMe": true,
          "remote": {
            "server": "c.us",
            "user": "5491160130996",
            "_serialized": "5491160130996@c.us"
          },
          "id": "3EB0B965CCCA5E15735D3A",
          "_serialized": "true_5491160130996@c.us_3EB0B965CCCA5E15735D3A"
        },
        "viewed": false,
        "body": "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",
        "type": "image",
        "t": 1704308228,
        "from": {
          "server": "c.us",
          "user": "5491130274052",
          "_serialized": "5491130274052@c.us"
        },
        "to": {
          "server": "c.us",
          "user": "5491160130996",
          "_serialized": "5491160130996@c.us"
        },
        "self": "out",
        "ack": 0,
        "isNewMsg": true,
        "star": false,
        "kicNotified": false,
        "deprecatedMms3Url": "https://mmg.whatsapp.net/o1/v/t62.7118-24/f1/m237/up-oil-image-107fa924-3be0-4f95-8202-c5af65fda9cc?ccb=9-4&oh=01_AdT2JbIKG0jFGz0rLTN0SA9Q-5NCL7r1CskLzmf24XKTpw&oe=65BD3385&_nc_sid=000000&mms3=true",
        "directPath": "/o1/v/t62.7118-24/f1/m237/up-oil-image-107fa924-3be0-4f95-8202-c5af65fda9cc?ccb=9-4&oh=01_AdT2JbIKG0jFGz0rLTN0SA9Q-5NCL7r1CskLzmf24XKTpw&oe=65BD3385&_nc_sid=000000",
        "mimetype": "image/jpeg",
        "filehash": "m/vnuBqWL/1bm5m6jATneokQ+RN4cg4EBIoJWMuxnZU=",
        "encFilehash": "G8PEFZqbywxDIxQuObokwhPzFQZ4j0mmHJ3E/GE5UNs=",
        "size": 39418,
        "mediaKey": "g+wXhPPaT8AkpgkOJ2ahAjnB04VmUa7NqMUImpOHhSY=",
        "mediaKeyTimestamp": 1704308227,
        "streamable": false,
        "isFromTemplate": false,
        "pollInvalidated": false,
        "isSentCagPollCreation": false,
        "latestEditMsgKey": null,
        "latestEditSenderTimestampMs": null,
        "mentionedJidList": [],
        "groupMentions": [],
        "isVcardOverMmsDocument": false,
        "isForwarded": false,
        "hasReaction": false,
        "disappearingModeInitiator": "chat",
        "disappearingModeTrigger": "chat_settings",
        "productHeaderImageRejected": false,
        "lastPlaybackProgress": 0,
        "isDynamicReplyButtonsMsg": false,
        "isCarouselCard": false,
        "parentMsgId": null,
        "isMdHistoryMsg": false,
        "stickerSentTs": 0,
        "lastUpdateFromServerTs": 0,
        "invokedBotWid": null,
        "bizBotType": null,
        "botResponseTargetId": null,
        "botPluginType": null,
        "botPluginReferenceIndex": null,
        "botPluginSearchProvider": null,
        "botPluginSearchUrl": null,
        "botPluginMaybeParent": false,
        "botReelPluginThumbnailCdnUrl": null,
        "botMsgBodyType": null,
        "requiresDirectConnection": null
      },
      "mediaKey": "g+wXhPPaT8AkpgkOJ2ahAjnB04VmUa7NqMUImpOHhSY=",
      "id": {
        "fromMe": true,
        "remote": {
          "server": "c.us",
          "user": "5491160130996",
          "_serialized": "5491160130996@c.us"
        },
        "id": "3EB0B965CCCA5E15735D3A",
        "_serialized": "true_5491160130996@c.us_3EB0B965CCCA5E15735D3A"
      },
      "ack": 0,
      "hasMedia": true,
      "body": "",
      "type": "image",
      "timestamp": 1704308228,
      "from": "5491130274052@c.us",
      "to": "5491160130996@c.us",
      "deviceType": "android",
      "isForwarded": false,
      "forwardingScore": 0,
      "isStatus": false,
      "isStarred": false,
      "fromMe": true,
      "hasQuotedMsg": false,
      "hasReaction": false,
      "vCards": [],
      "mentionedIds": [],
      "isGif": false
    }
  },
  "links": {
    "self": "https://waapi.app/api/v1/instances/4107/client/action/send-media"
  },
  "status": "success"
'''