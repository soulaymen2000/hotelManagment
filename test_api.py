import requests
import json

# Test the login endpoint
url = "http://127.0.0.1:8000/api/auth/login/"
data = {
    "email": "admin@hotel.com",
    "password": "admin123"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())