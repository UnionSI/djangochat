import requests

apiURL = 'https://7103.api.greenapi.com'
idInstance = '7103880835'
apiTokenInstance = '89bddd8da48246f593916d55b8be98e059a136b7b7e6469291'

url = f"https://api.green-api.com/waInstance{idInstance}/sendMessage/{apiTokenInstance}"

payload = "{\r\n\t\"chatId\": \"5491160130996@c.us\",\r\n\t\"message\": \"I use Green-API to send this message to you!\"\r\n}"
headers = {
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))


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