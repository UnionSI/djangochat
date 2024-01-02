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
    id_instance = "3901"
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