import requests


def setup_demo_user():
    """Setup the demo user."""
    response = requests.post(
        "http://localhost:8000/auth/setup-demo",
        timeout=10,
    )
    print(f"Setup Status: {response.status_code}")
    print(f"Setup Response: {response.text}")
    return response


def login_demo_user():
    """Login with the demo user and get a token."""
    response = requests.post(
        "http://localhost:8000/auth/login",
        json={"email": "demo@example.com", "password": "demodemo"},
        timeout=10,
    )
    print(f"Login Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        print("Login successful!")
        print(f"Token: {token_data['access_token']}")
        return token_data["access_token"]
    else:
        print(f"Login failed: {response.text}")
        return None


def test_protected_endpoint(token):
    """Test accessing a protected endpoint with the token."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "http://localhost:8000/leads/",
        headers=headers,
        timeout=10,
    )
    print(f"Leads Status: {response.status_code}")
    print(f"Leads Response: {response.text}")
    return response


if __name__ == "__main__":
    print("Setting up demo user...")
    setup_demo_user()

    print("\nLogging in demo user...")
    token = login_demo_user()

    if token:
        print("\nTesting protected endpoint...")
        test_protected_endpoint(token)
