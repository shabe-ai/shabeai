from app.models import Company
from app.services.company_service import CompanyService


def test_company_service_list_companies(session):
    """Test listing companies through the service"""
    # Create some companies
    companies = [
        Company(name="Acme Corp", website="https://acme.com"),
        Company(name="Tech Solutions", website="https://techsolutions.com"),
    ]
    for company in companies:
        session.add(company)
    session.commit()

    service = CompanyService(session)
    all_companies = service.list()
    assert len(all_companies) >= 2
    names = [company.name for company in all_companies]
    assert "Acme Corp" in names
    assert "Tech Solutions" in names


def test_company_service_get_company(session):
    """Test getting a company by ID through the service"""
    # Create a company first
    company = Company(name="Test Company 1", website="https://test.com")
    session.add(company)
    session.commit()
    session.refresh(company)

    service = CompanyService(session)
    retrieved_company = service.get(company.id)
    assert retrieved_company.id == company.id
    assert retrieved_company.name == "Test Company 1"


def test_company_service_get_company_not_found(session):
    """Test getting a company that doesn't exist"""
    service = CompanyService(session)
    result = service.get("non-existent-id")
    assert result is None


def test_company_service_create_company(session):
    """Test creating a company through the service"""
    service = CompanyService(session)
    company_data = {"name": "New Company 1", "website": "https://newcompany.com"}

    company = service.create(company_data)
    assert company.name == "New Company 1"
    assert company.website == "https://newcompany.com"
    assert company.id is not None


def test_company_service_update_company(session):
    """Test updating a company through the service"""
    # Create a company first
    company = Company(name="Original 1", website="https://original.com")
    session.add(company)
    session.commit()
    session.refresh(company)

    service = CompanyService(session)
    update_data = {"name": "Updated 1", "website": "https://updated.com"}

    updated_company = service.update(company, update_data)
    assert updated_company.name == "Updated 1"
    assert updated_company.website == "https://updated.com"


def test_company_service_delete_company(session):
    """Test deleting a company through the service"""
    # Create a company first
    company = Company(name="Delete Me 1", website="https://deleteme.com")
    session.add(company)
    session.commit()
    session.refresh(company)

    service = CompanyService(session)
    service.delete(company)

    # Verify it's deleted
    result = service.get(company.id)
    assert result is None
