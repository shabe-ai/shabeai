import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.database import engine
from app.main import app, get_session
from app.models import Company, Lead


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    # create fresh schema once for the session
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture()
def session():
    with Session(engine) as s:
        yield s        # empty session per-test → no state bleed

def _override_session():
    with Session(engine) as s:
        yield s

app.dependency_overrides[get_session] = _override_session

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def auth_headers(client):
    # Register user (ignore if already exists)
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
        },
    )
    # Login user
    resp = client.post(
        "/auth/jwt/login",
        data={"username": "test@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 204
    # Return cookie for authenticated requests
    cookie = resp.cookies.get("crm-auth")
    return {"Cookie": f"crm-auth={cookie}"} if cookie else {}

@pytest.fixture()
def sample_company(session):
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
        website="https://testcompany.com",
        linkedinUrl="https://linkedin.com/company/test"
    )
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

@pytest.fixture()
def sample_lead(session, sample_company):
    lead = Lead(
        id=str(uuid.uuid4()),
        firstName="John",
        lastName="Doe",
        email="test@example.com",
        phone="+1234567890",
        companyId=sample_company.id,
    )
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead 