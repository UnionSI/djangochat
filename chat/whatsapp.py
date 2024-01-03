import httpx, json


async def enviar_mensaje_greenapi(chat_id, message):
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


async def enviar_mensaje_waapi(chat_id, message):
    # webhook: https://djangochat-1.onrender.com/contacto/waapi_api_webhook
    id_instance = "4107"
    api_name = "customer-service"
    api_token_instance = "ipiOhK708cW4DuUHNtd234FnnnsfWyujgjV2S7THeac23b4f"

    url = f'https://waapi.app/api/v1/instances/{id_instance}/client/action/send-message'

    payload = {
        "chatId": f"{chat_id}@c.us",
        "message": message
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {api_token_instance}'
    }

    async with httpx.AsyncClient() as client:
        #response = await client.post(url, json=json.dumps(payload), headers=headers)
        response = await client.post(url, json=payload, headers=headers)

    return response.json()


async def enviar_adjunto_waapi(chat_id, message, mediafile):
    # webhook: https://djangochat-1.onrender.com/contacto/waapi_api_webhook
    id_instance = "4107"
    api_name = "customer-service"
    api_token_instance = "ipiOhK708cW4DuUHNtd234FnnnsfWyujgjV2S7THeac23b4f"

    url = f'https://waapi.app/api/v1/instances/{id_instance}/client/action/send-media'

    payload = {
        "mediaUrl": "https://www.freepnglogos.com/uploads/google-logo-png/google-logo-png-suite-everything-you-need-know-about-google-newest-0.png",
        "mediaCaption": "This is a test image",
        "mediaName": "imageName.png",
        "chatId": f"{chat_id}@c.us",
        #"message": message
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {api_token_instance}'
    }

    async with httpx.AsyncClient() as client:
        #response = await client.post(url, json=json.dumps(payload), headers=headers)
        response = await client.post(url, json=payload, headers=headers)

    return response.json()

'''
mediafiles

import requests

url = "https://waapi.app/api/v1/instances/4107/client/action/send-media"

payload = {
    "mediaUrl": "https://waapi.app/android-chrome-192x192.png",
    "mediaCaption": "This is a test image",
    "mediaName": "imageName.png",
    "chatId": "5491160130996@c.us"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer ipiOhK708cW4DuUHNtd234FnnnsfWyujgjV2S7THeac23b4f"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
'''