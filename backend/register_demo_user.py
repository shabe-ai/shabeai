import requests

print("Registering demo user...")
url = "http://localhost:8000/custom-auth/register"
data = {
    "email": "demo@example.com",
    "password": "demodemo"
}

response = requests.post(url, json=data)
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")

print("\nLogging in demo user...")
login_url = "http://localhost:8000/custom-auth/login"
login_data = {
    "email": "demo@example.com",
    "password": "demodemo"
}

login_response = requests.post(login_url, json=login_data)
print(f"Login Status code: {login_response.status_code}")
if login_response.status_code == 200:
    print("Login successful!")
    print(f"Token: {login_response.json()}")
else:
    print(f"Login failed: {login_response.text}") 