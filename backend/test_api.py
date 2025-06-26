import requests
import json

# Test login with FastAPI Users
print("Testing login...")
login_data = {
    "username": "demo@example.com",
    "password": "demodemo"
}

# Try the FastAPI Users login endpoint (uses form data)
response = requests.post("http://localhost:8000/auth/jwt/login", data=login_data)
print(f"Login status: {response.status_code}")
print(f"Login response: {response.text}")

if response.status_code == 200:
    token_data = response.json()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test users endpoint
    print("\nTesting users endpoint...")
    users_response = requests.get("http://localhost:8000/users/me", headers=headers)
    print(f"Users status: {users_response.status_code}")
    print(f"Users response: {users_response.text}")
else:
    print("Login failed, trying to register demo user...")
    
    # Try to register the demo user
    register_data = {
        "email": "demo@example.com",
        "password": "demodemo",
        "full_name": "Demo User"
    }
    
    register_response = requests.post("http://localhost:8000/auth/register", json=register_data)
    print(f"Register status: {register_response.status_code}")
    print(f"Register response: {register_response.text}") 