from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_companies():
    response = client.get("/companies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_company():
    data = {"name": "Coverage Co", "website": "https://coverageco.com"}
    response = client.post("/companies/", json=data)
    assert response.status_code == 201
    company = response.json()
    assert company["name"] == "Coverage Co"
    assert company["website"] == "https://coverageco.com" 