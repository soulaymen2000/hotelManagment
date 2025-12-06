import requests
import json

url = 'http://127.0.0.1:8000/api/auth/login/'
data = {
    'email': 'sou@gmail.com',
    'password': 'azerty123456'
}

response = requests.post(url, json=data)
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')