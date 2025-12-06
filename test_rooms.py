import requests
import json

# First, login to get the access token
login_url = "http://127.0.0.1:8000/api/auth/login/"
login_data = {
    "email": "admin@hotel.com",
    "password": "admin123"
}

login_response = requests.post(login_url, json=login_data)
access_token = login_response.json()['access']

# Test the rooms endpoint
rooms_url = "http://127.0.0.1:8000/api/rooms/"
headers = {
    "Authorization": f"Bearer {access_token}"
}

rooms_response = requests.get(rooms_url, headers=headers)
print("Status Code:", rooms_response.status_code)
print("Rooms:", json.dumps(rooms_response.json(), indent=2))