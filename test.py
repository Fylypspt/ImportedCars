import requests
import os

# Se quiseres, podes meter isto num .env e usar load_dotenv
ACCESS_TOKEN = "EAAKyUIh7TLsBPd1dhs0uCCuO4Ey2TqtZCT5CKOIqZClY7NSkZCrQTSZA5pCEGfZBZCI0IQ8JX0XGLcRQZATluWL1gjJEoP5V7fSVd6U3OlUcia73eyNL05tA5NwH4OmEYV0xMaVKUTn34MpZBPfGH4muXY00dMTl4HPBr1k4Pz7G9LZAR9nKkIGdZABIDWZBO1fbpba90fJUha1Vk8ypYOviejN1nQOWICQcwbhN7KkkXBy"
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
