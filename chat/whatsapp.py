import httpx, json


async def send_greenapi_message(self, chat_id, message):
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


async def send_waapi_message(self, chat_id, message):
    id_instance = "3554"
    api_name = "ETBu4KVOMXT2KCL1t9SGRIJ7Ra8zEPFM60QINdAp3GjD5Ba"
    api_token_instance = "XtkLU4toIS8PzXdZGjQIUFOUzhFzxxmcUqoVCRwUd46d9dc9"

    url = f'https://api.greenapi.com/waInstance{id_instance}/sendMessage/{api_token_instance}'

    payload = {
        "chatId": f"{chat_id}@c.us",
        "message": message
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer XtkLU4toIS8PzXdZGjQIUFOUzhFzxxmcUqoVCRwUd46d9dc9"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=json.dumps(payload), headers=headers)

    return response.json()