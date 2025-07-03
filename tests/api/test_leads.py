import pytest
from fastapi import status
from ..factories import LeadFactory, valid_lead_payload

class TestLeadsAPI:
    """Test suite for the Leads API endpoints."""
    
    def test_create_lead_success(self, client, auth_headers):
        """Test successful lead creation."""
        payload = LeadFactory.create()
        response = client.post("/leads/", json=payload, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == payload["email"]
        assert data["firstName"] == payload["firstName"]
        assert data["lastName"] == payload["lastName"]
        assert "id" in data
        assert "createdAt" in data
    
    def test_create_lead_duplicate_email(self, client, auth_headers, session):
        """Test lead creation with duplicate email fails."""
        # Create first lead
        lead = LeadFactory.create_model(session)
        
        # Try to create second lead with same email
        payload = LeadFactory.create(email=lead.email)
        response = client.post("/leads/", json=payload, headers=auth_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_list_leads_empty(self, client, auth_headers):
        """Test listing leads when none exist."""
        response = client.get("/leads/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_list_leads_with_data(self, client, auth_headers, session):
        """Test listing leads with existing data."""
        # Create test leads
        lead1 = LeadFactory.create_model(session)
        lead2 = LeadFactory.create_model(session)
        
        response = client.get("/leads/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert any(lead["email"] == lead1.email for lead in data)
        assert any(lead["email"] == lead2.email for lead in data)
    
    def test_get_lead_by_id(self, client, auth_headers, session):
        """Test retrieving a specific lead by ID."""
        lead = LeadFactory.create_model(session)
        
        response = client.get(f"/leads/{lead.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == lead.id
        assert data["email"] == lead.email
    
    def test_get_lead_not_found(self, client, auth_headers):
        """Test retrieving a non-existent lead."""
        fake_id = "non-existent-id"
        response = client.get(f"/leads/{fake_id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_lead(self, client, auth_headers, session):
        """Test updating a lead."""
        lead = LeadFactory.create_model(session)
        update_data = {"firstName": "Updated", "phone": "+1234567890"}
        
        response = client.put(f"/leads/{lead.id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["firstName"] == "Updated"
        assert data["phone"] == "+1234567890"
        assert data["email"] == lead.email  # Unchanged
    
    def test_delete_lead(self, client, auth_headers, session):
        """Test deleting a lead."""
        lead = LeadFactory.create_model(session)
        
        response = client.delete(f"/leads/{lead.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify lead is deleted
        get_response = client.get(f"/leads/{lead.id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

class TestLeadValidation:
    """Test suite for lead validation."""
    
    @pytest.mark.parametrize("missing_field", ["email", "firstName", "lastName"])
    def test_create_lead_missing_required_fields(self, client, auth_headers, missing_field):
        """Test lead creation fails when required fields are missing."""
        data = valid_lead_payload.copy()
        data.pop(missing_field)
        
        response = client.post("/leads/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @pytest.mark.parametrize("invalid_email", [
        "not-an-email",
        "missing@",
        "@missing-domain.com",
        "spaces @example.com",
        ""
    ])
    def test_create_lead_invalid_email(self, client, auth_headers, invalid_email):
        """Test lead creation fails with invalid email formats."""
        data = valid_lead_payload.copy()
        data["email"] = invalid_email
        
        response = client.post("/leads/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_lead_empty_strings(self, client, auth_headers):
        """Test lead creation fails with empty required strings."""
        data = valid_lead_payload.copy()
        data.update({
            "firstName": "",
            "lastName": "",
            "email": ""
        })
        
        response = client.post("/leads/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_lead_optional_fields(self, client, auth_headers):
        """Test lead creation succeeds with only required fields."""
        data = {
            "email": "test@example.com",
            "firstName": "John",
            "lastName": "Doe"
        }
        
        response = client.post("/leads/", json=data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["phone"] is None
        assert response_data["linkedinUrl"] is None
        assert response_data["companyId"] is None

class TestLeadAuthentication:
    """Test suite for lead authentication requirements."""
    
    def test_create_lead_without_auth(self, client):
        """Test lead creation fails without authentication."""
        payload = LeadFactory.create()
        response = client.post("/leads/", json=payload)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_leads_without_auth(self, client):
        """Test listing leads fails without authentication."""
        response = client.get("/leads/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_lead_without_auth(self, client):
        """Test getting lead fails without authentication."""
        response = client.get("/leads/some-id")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_lead_without_auth(self, client):
        """Test updating lead fails without authentication."""
        response = client.put("/leads/some-id", json={"firstName": "Updated"})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_lead_without_auth(self, client):
        """Test deleting lead fails without authentication."""
        response = client.delete("/leads/some-id")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 