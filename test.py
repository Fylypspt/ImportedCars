import requests
import os

# Se quiseres, podes meter isto num .env e usar load_dotenv
ACCESS_TOKEN = "EAAKyUIh7TLsBPaVEavqvTs9kyFZCi7cS7SL4OQHyumgRvx4vVbJyJZAUSymksL7xuNm5sj0HCk6A2r5kzNQ5oGdfPe5nQynzc1Wr8TvBAk9qs9DwMZAdZBZCjqe5x6n6uiQHCgRCQ0AvzoAhPyRjxoiG7kYwcyNbZBnnFnh4wEoqrq1awZCg26sggb42cNP3oWq7W3o7cCXZBZB0SExfaILckzTiyftvBT9aDueWYGkO44gWz7QZDZD"
PHONE_NUMBER_ID = "698802006660937"   # O teu Phone Number ID
TO_NUMBER = "351963755484"            # O teu número em formato internacional (sem +)

url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Aqui estamos a usar o template "hello_world" que já vem ativado no teu WhatsApp Cloud API
payload = {
    "messaging_product": "whatsapp",
    "to": TO_NUMBER,
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": { "code": "en_US" }
    }
}

res = requests.post(url, headers=headers, json=payload)

print("Status:", res.status_code)
print("Response:", res.json())
