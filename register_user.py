import requests

response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "email": "alice@example.com",
        "password": "Passw0rd!"
    }
)

print("Status Code:", response.status_code)
print("Response:", response.text) 