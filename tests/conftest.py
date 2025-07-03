import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from faker import Faker

from app.main import app
from app.database import get_session

# Initialize Faker for test data generation
fake = Faker()

@pytest.fixture(scope="session")
def engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine) -> Generator[Session, None, None]:
    """Create a database session for each test."""
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session) -> TestClient:
    """Create a test client with dependency overrides."""
    
    def override_get_session():
        yield session
    
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)

@pytest.fixture
def demo_user(client) -> dict:
    """Create a demo user and return auth data."""
    data = {"email": "demo@example.com", "password": "p@ssw0rd"}
    client.post("/auth/register", json=data)
    login = client.post("/auth/jwt/login", data={
        "username": data["email"], 
        "password": data["password"]
    })
    token = login.cookies.get("crm-auth")
    return {"email": data["email"], "token": token}

@pytest.fixture
def auth_headers(demo_user) -> dict:
    """Return headers with authentication token."""
    return {"Authorization": f"Bearer {demo_user['token']}"}

@pytest.fixture(autouse=True)
def _no_external_calls(monkeypatch):
    """Prevent external API calls during tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    # Prevent real OpenAI imports - use a safer approach
    try:
        monkeypatch.setattr("builtins.openai", None)
    except AttributeError:
        # If openai doesn't exist in builtins, that's fine
        pass 