import requests

apiURL = 'https://7103.api.greenapi.com'
idInstance = '7103879408'
apiTokenInstance = 'b5481b0a67bc4483b914eaa275c38d648fda39787fb04d0ea5'

url = f"https://api.green-api.com/waInstance{idInstance}/sendMessage/{apiTokenInstance}"

payload = "{\r\n\t\"chatId\": \"5491160130996@c.us\",\r\n\t\"message\": \"I use Green-API to send this message to you!\"\r\n}"
headers = {
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))