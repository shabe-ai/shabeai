import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_task():
    # Create a lead first
    lead_data = {"firstName": "TaskCoverage", "lastName": "User", "email": "taskcoverage@example.com"}
    lead_resp = client.post("/leads/", json=lead_data)
    assert lead_resp.status_code == 201
    lead_id = lead_resp.json()["id"]
    data = {"title": "Coverage Task", "dueDate": "2030-01-01T00:00:00Z", "isDone": False, "leadId": lead_id}
    response = client.post("/tasks/", json=data)
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Coverage Task"
    assert task["leadId"] == lead_id 