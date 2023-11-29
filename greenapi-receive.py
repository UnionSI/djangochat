import requests

apiURL = 'https://7103.api.greenapi.com'
idInstance = '7103880835'
apiTokenInstance = '89bddd8da48246f593916d55b8be98e059a136b7b7e6469291'

url = f'https://api.green-api.com/waInstance{idInstance}/receiveNotification/{apiTokenInstance}'

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))

url = f'https://api.green-api.com/waInstance{idInstance}/deleteNotification/{apiTokenInstance}/1234567'

payload = {}
headers= {}

response = requests.request("DELETE", url, headers=headers, data = payload)

print(response.text.encode('utf8'))