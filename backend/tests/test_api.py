def test_login_and_me(client):
    # 1. register
    r = client.post(
        "/auth/register",
        json={
            "email": "demo@example.com",
            "password": "demodemo",
            "full_name": "Demo User",
        },
    )
    print(f"Registration response: {r.status_code}")
    print(f"Registration body: {r.text}")
    assert r.status_code == 201

    # 2. login
    r = client.post(
        "/auth/jwt/login",
        data={"username": "demo@example.com", "password": "demodemo"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 204
    cookie = r.cookies.get("crm-auth")
    assert cookie

    # 3. /users/me with the cookie
    r = client.get("/users/me", cookies={"crm-auth": cookie})
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "demo@example.com"


def test_leads_list(client, session):
    # seed one lead (using your SQLModel ORM)
    from app.models import Lead

    lead = Lead(firstName="John", lastName="Doe", email="john@acme.dev")
    session.add(lead)
    session.commit()

    r = client.get("/leads/")
    assert r.status_code == 200
    assert len(r.json()) >= 1
