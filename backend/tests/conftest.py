import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from app.main import app
from app.deps import get_db
from app.models import Lead, Company, Deal, Task

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_db_override():
        yield session
    
    app.dependency_overrides[get_db] = get_db_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="auth_headers")
def auth_headers_fixture():
    # Mock authentication headers - replace with actual auth logic
    return {"Authorization": "Bearer test-token"}

@pytest.fixture(name="sample_company")
def sample_company_fixture(session: Session):
    company = Company(
        name="Test Company",
        website="https://testcompany.com",
        linkedinUrl="https://linkedin.com/company/test"
    )
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

@pytest.fixture(name="sample_lead")
def sample_lead_fixture(session: Session, sample_company):
    lead = Lead(
        email="test@example.com",
        firstName="John",
        lastName="Doe",
        phone="+1234567890",
        companyId=sample_company.id
    )
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead 