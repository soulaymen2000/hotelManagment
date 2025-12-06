import requests
import json

# Test the login endpoint
url = "http://127.0.0.1:8000/api/auth/login/"
data = {
    "email": "sou@gmail.com",
    "password": "azerty123456"
}

print("Sending login request...")
print(f"URL: {url}")
print(f"Data: {data}")

response = requests.post(url, json=data)

print(f"\nResponse Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Text: {response.text}")

try:
    response_data = response.json()
    print(f"Response JSON: {json.dumps(response_data, indent=2)}")
except Exception as e:
    print(f"Could not parse JSON: {e}")