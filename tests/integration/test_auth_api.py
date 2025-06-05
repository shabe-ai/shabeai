import uuid

def test_register_and_login(client):
    # Use a unique email to avoid conflicts
    email = f"test_{uuid.uuid4()}@example.com"
    r = client.post("/auth/register",
                    json={"email": email, "password": "secret"})
    if r.status_code != 201:
        print(f"Registration failed: {r.json()}")
    assert r.status_code == 201

    r = client.post("/auth/jwt/login",
                    data={"username": email, "password": "secret"})
    assert r.status_code in (200, 204)
    assert "crm-auth" in r.cookies 