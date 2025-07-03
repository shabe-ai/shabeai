from fastapi import status
from ..factories import LeadFactory, CompanyFactory

def test_basic_fixtures(client, session):
    """Test that basic fixtures work."""
    assert client is not None
    assert session is not None

def test_lead_factory():
    """Test that LeadFactory works."""
    lead_data = LeadFactory.create()
    assert "email" in lead_data
    assert "firstName" in lead_data
    assert "lastName" in lead_data
    assert lead_data["email"] != ""
    assert lead_data["firstName"] != ""
    assert lead_data["lastName"] != ""

def test_company_factory():
    """Test that CompanyFactory works."""
    company_data = CompanyFactory.create()
    assert "name" in company_data
    assert "website" in company_data
    assert company_data["name"] != ""
    assert company_data["website"] != ""

def test_lead_model_creation(session):
    """Test creating a Lead model in the database."""
    lead = LeadFactory.create_model(session)
    assert lead.id is not None
    assert lead.email is not None
    assert lead.firstName is not None
    assert lead.lastName is not None

def test_company_model_creation(session):
    """Test creating a Company model in the database."""
    company = CompanyFactory.create_model(session)
    assert company.id is not None
    assert company.name is not None

def test_health_endpoint(client):
    """Test the health endpoint works."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json() 