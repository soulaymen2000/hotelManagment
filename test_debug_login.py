import requests
import json

# Test the login endpoint with detailed logging
url = "http://127.0.0.1:8000/api/auth/login/"
data = {
    "email": "admin@hotel.com",
    "password": "admin123"
}

print("Sending login request...")
print(f"URL: {url}")
print(f"Data: {data}")

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")

try:
    response_data = response.json()
    print(f"Response JSON: {json.dumps(response_data, indent=2)}")
except Exception as e:
    print(f"Could not parse JSON: {e}")
    print(f"Response Text: {response.text}")

# Also test the template-based login
print("\n" + "="*50)
print("Testing template-based login...")

template_url = "http://127.0.0.1:8000/accounts/login/"
response2 = requests.post(template_url, data=data)
print(f"Template Login Status Code: {response2.status_code}")
print(f"Template Login Response Headers: {dict(response2.headers)}")

try:
    response_data2 = response2.json()
    print(f"Template Login Response JSON: {json.dumps(response_data2, indent=2)}")
except Exception as e:
    print(f"Could not parse JSON: {e}")
    print(f"Template Login Response Text: {response2.text[:500]}...")  # First 500 chars