from app.models import Lead
from app.schemas.lead import LeadCreate
from app.services.lead_service import LeadService


def test_lead_service_list_leads(session):
    """Test listing leads through the service"""
    # Create some leads
    leads = [
        Lead(firstName="Alice", lastName="Johnson", email="alice1@example.com"),
        Lead(firstName="Bob", lastName="Brown", email="bob1@example.com")
    ]
    for lead in leads:
        session.add(lead)
    session.commit()
    
    service = LeadService(session)
    all_leads = service.list()
    assert len(all_leads) >= 2
    emails = [lead.email for lead in all_leads]
    assert "alice1@example.com" in emails
    assert "bob1@example.com" in emails


def test_lead_service_get_lead(session):
    """Test getting a lead by ID through the service"""
    # Create a lead first
    lead = Lead(firstName="John", lastName="Doe", email="john1@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    service = LeadService(session)
    retrieved_lead = service.get(lead.id)
    assert retrieved_lead.id == lead.id
    assert retrieved_lead.email == "john1@example.com"


def test_lead_service_get_lead_not_found(session):
    """Test getting a lead that doesn't exist"""
    service = LeadService(session)
    result = service.get("non-existent-id")
    assert result is None  # The service returns None for non-existent leads


def test_lead_service_create_lead(session):
    """Test creating a lead through the service"""
    service = LeadService(session)
    lead_data = LeadCreate(
        firstName="Jane",
        lastName="Smith",
        email="jane1@example.com"
    )
    
    # Convert to dict since the service expects model_dump()
    # lead_dict = {
    #     "firstName": lead_data.firstName,
    #     "lastName": lead_data.lastName,
    #     "email": lead_data.email
    # }
    
    lead = service.create(lead_data)
    assert lead.firstName == "Jane"
    assert lead.email == "jane1@example.com"
    assert lead.id is not None


def test_lead_service_update_lead(session):
    """Test updating a lead through the service"""
    # Create a lead first
    lead = Lead(firstName="Original", lastName="Name", email="original1@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    service = LeadService(session)
    from app.schemas.lead import LeadCreate
    update_data = LeadCreate(
        firstName="Updated", lastName="Name", email="updated1@example.com"
    )
    
    updated_lead = service.update(lead, update_data)
    assert updated_lead.firstName == "Updated"
    assert updated_lead.email == "updated1@example.com"


def test_lead_service_delete_lead(session):
    """Test deleting a lead through the service"""
    # Create a lead first
    lead = Lead(firstName="Delete", lastName="Me", email="delete1@example.com")
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    service = LeadService(session)
    service.delete(lead)
    
    # Verify it's deleted
    result = service.get(lead.id)
    assert result is None 