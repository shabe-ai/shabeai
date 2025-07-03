from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_setup_demo():
    response = client.post("/auth/setup-demo")
    assert response.status_code == 200
    assert response.json()["message"] == "Demo user setup complete"


def test_list_users():
    # Ensure at least one user exists
    client.post("/auth/setup-demo")
    response = client.get("/auth/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(user["email"] == "demo@example.com" for user in users)
