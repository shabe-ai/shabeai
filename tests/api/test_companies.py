import pytest
from fastapi import status
from tests.factories import CompanyFactory, LeadFactory, DealFactory, valid_company_payload

class TestCompaniesAPI:
    """Test suite for the Companies API endpoints."""
    
    def test_create_company_success(self, client, auth_headers):
        """Test successful company creation."""
        payload = CompanyFactory.create()
        response = client.post("/companies/", json=payload, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["website"] == payload["website"]
        assert data["linkedinUrl"] == payload["linkedinUrl"]
        assert "id" in data
        assert "createdAt" in data
    
    def test_create_company_duplicate_name(self, client, auth_headers, session):
        """Test company creation with duplicate name fails."""
        # Create first company
        company = CompanyFactory.create_model(session)
        
        # Try to create second company with same name
        payload = CompanyFactory.create(name=company.name)
        response = client.post("/companies/", json=payload, headers=auth_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_list_companies_empty(self, client, auth_headers):
        """Test listing companies when none exist."""
        response = client.get("/companies/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_list_companies_with_data(self, client, auth_headers, session):
        """Test listing companies with existing data."""
        # Create test companies
        company1 = CompanyFactory.create_model(session)
        company2 = CompanyFactory.create_model(session)
        
        response = client.get("/companies/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert any(c["name"] == company1.name for c in data)
        assert any(c["name"] == company2.name for c in data)
    
    def test_get_company_by_id(self, client, auth_headers, session):
        """Test retrieving a specific company by ID."""
        company = CompanyFactory.create_model(session)
        
        response = client.get(f"/companies/{company.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == company.id
        assert data["name"] == company.name
    
    def test_get_company_not_found(self, client, auth_headers):
        """Test retrieving a non-existent company."""
        fake_id = "non-existent-id"
        response = client.get(f"/companies/{fake_id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_company(self, client, auth_headers, session):
        """Test updating a company."""
        company = CompanyFactory.create_model(session)
        update_data = {"name": "Updated Company", "website": "https://updated.com"}
        
        response = client.put(f"/companies/{company.id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Company"
        assert data["website"] == "https://updated.com"
        assert data["linkedinUrl"] == company.linkedinUrl  # Unchanged
    
    def test_delete_company(self, client, auth_headers, session):
        """Test deleting a company."""
        company = CompanyFactory.create_model(session)
        
        response = client.delete(f"/companies/{company.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify company is deleted
        get_response = client.get(f"/companies/{company.id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

class TestCompanyValidation:
    """Test suite for company validation."""
    
    @pytest.mark.parametrize("missing_field", ["name"])
    def test_create_company_missing_required_fields(self, client, auth_headers, missing_field):
        """Test company creation fails when required fields are missing."""
        data = valid_company_payload.copy()
        data.pop(missing_field)
        
        response = client.post("/companies/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @pytest.mark.parametrize("invalid_url", [
        "not-a-url",
        "ftp://invalid-protocol.com",
        "missing-protocol.com",
        "http://",
        ""
    ])
    def test_create_company_invalid_urls(self, client, auth_headers, invalid_url):
        """Test company creation with invalid URL formats."""
        data = valid_company_payload.copy()
        data["website"] = invalid_url
        
        response = client.post("/companies/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_company_empty_name(self, client, auth_headers):
        """Test company creation fails with empty name."""
        data = valid_company_payload.copy()
        data["name"] = ""
        
        response = client.post("/companies/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_company_optional_fields(self, client, auth_headers):
        """Test company creation succeeds with only required fields."""
        data = {"name": "Test Company"}
        
        response = client.post("/companies/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["website"] is None
        assert response_data["linkedinUrl"] is None

class TestCompanyRelationships:
    """Test suite for company relationships with leads and deals."""
    
    def test_company_with_leads(self, client, auth_headers, session):
        """Test company can have associated leads."""
        company = CompanyFactory.create_model(session)
        LeadFactory.create_model(session, companyId=company.id)
        LeadFactory.create_model(session, companyId=company.id)
        
        response = client.get(f"/companies/{company.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data.get("leads", [])) == 2
    
    def test_company_with_deals(self, client, auth_headers, session):
        """Test company can have associated deals."""
        company = CompanyFactory.create_model(session)
        DealFactory.create_model(session, company.id)
        DealFactory.create_model(session, company.id)
        
        response = client.get(f"/companies/{company.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data.get("deals", [])) == 2
    
    def test_delete_company_with_relationships(self, client, auth_headers, session):
        """Test deleting company with relationships (should fail or cascade)."""
        company = CompanyFactory.create_model(session)
        LeadFactory.create_model(session, companyId=company.id)
        DealFactory.create_model(session, company.id)
        
        response = client.delete(f"/companies/{company.id}", headers=auth_headers)
        
        # This might fail due to foreign key constraints, or cascade delete
        # The exact behavior depends on your database configuration
        assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_400_BAD_REQUEST]

class TestCompanyAuthentication:
    """Test suite for company authentication requirements."""
    
    def test_create_company_without_auth(self, client):
        """Test company creation fails without authentication."""
        payload = CompanyFactory.create()
        response = client.post("/companies/", json=payload)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_companies_without_auth(self, client):
        """Test listing companies fails without authentication."""
        response = client.get("/companies/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_company_without_auth(self, client):
        """Test getting company fails without authentication."""
        response = client.get("/companies/some-id")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_company_without_auth(self, client):
        """Test updating company fails without authentication."""
        response = client.put("/companies/some-id", json={"name": "Updated"})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_company_without_auth(self, client):
        """Test deleting company fails without authentication."""
        response = client.delete("/companies/some-id")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 