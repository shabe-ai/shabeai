import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_deals():
    response = client.get("/deals/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_deal():
    # Create a company first
    company_data = {"name": "Deal Coverage Co", "website": "https://dealcoverage.com"}
    company_resp = client.post("/companies/", json=company_data)
    assert company_resp.status_code == 201
    company_id = company_resp.json()["id"]
    data = {"title": "Coverage Deal", "value": 12345, "stage": "new", "companyId": company_id}
    response = client.post("/deals/", json=data)
    assert response.status_code == 201
    deal = response.json()
    assert deal["title"] == "Coverage Deal"
    assert deal["companyId"] == company_id 