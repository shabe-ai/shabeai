import pytest, uuid, os
from fastapi.testclient import TestClient
from app.auth import api as app
from app.database import get_session
from sqlalchemy_utils import create_database, database_exists, drop_database
import builtins

@pytest.fixture(scope="session", autouse=True)
def _fresh_db(tmp_path_factory):
    # create a dedicated sqlite file per test session
    db_path = tmp_path_factory.mktemp("data") / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    init_db()
    yield
    # nothing to clean—sqlite file disappears with tmp dir

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def demo_user(client):
    data = {"email": "demo@example.com", "password": "p@ssw0rd"}
    client.post("/auth/register", json=data)
    login = client.post("/auth/jwt/login", data={"username": data["email"], "password": data["password"]})
    token = login.cookies.get("crm-auth")
    return {"email": data["email"], "token": token}

@pytest.fixture(autouse=True)
def _no_external_calls(monkeypatch):
    """Prevent external API calls during tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setitem(builtins.__dict__, "openai", None)  # crude: prevents real import 