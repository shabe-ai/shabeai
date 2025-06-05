import requests

def register_user(email: str, password: str):
    """Register a new user with the provided credentials."""
    response = requests.post(
        "http://localhost:8000/auth/register",
        json={
            "email": email,
            "password": password,
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
        },
        timeout=5,
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    return response

if __name__ == "__main__":
    register_user("alice@example.com", "Passw0rd!") 