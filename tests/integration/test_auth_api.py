def test_register_and_login(client):
    r = client.post("/auth/register",
                    json={"email": "a@b.com", "password": "secret"})
    assert r.status_code == 201
    login = client.post("/auth/jwt/login",
                        data={"username": "a@b.com", "password": "secret"})
    assert login.status_code in (200, 204)
    assert "crm-auth" in login.cookies 