import requests

apiURL = 'https://7103.api.greenapi.com'
idInstance = '7103879408'
apiTokenInstance = 'b5481b0a67bc4483b914eaa275c38d648fda39787fb04d0ea5'

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