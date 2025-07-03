import pytest
from unittest.mock import Mock, patch
from app.services.deal_service import DealService
from app.models import Deal, Company


def test_deal_service_list_deals(session):
    """Test listing deals through the service"""
    # Create a company first
    company = Company(name="Test Company List", website="https://testlist.com")
    session.add(company)
    session.commit()
    session.refresh(company)
    
    # Create some deals
    deals = [
        Deal(title="Deal 1", value=10000, stage="new", companyId=company.id),
        Deal(title="Deal 2", value=20000, stage="proposal", companyId=company.id)
    ]
    for deal in deals:
        session.add(deal)
    session.commit()
    
    service = DealService(session)
    all_deals = service.list()
    assert len(all_deals) >= 2
    titles = [deal.title for deal in all_deals]
    assert "Deal 1" in titles
    assert "Deal 2" in titles


def test_deal_service_get_deal(session):
    """Test getting a deal by ID through the service"""
    # Create a company first
    company = Company(name="Test Company Get", website="https://testget.com")
    session.add(company)
    session.commit()
    session.refresh(company)
    
    # Create a deal
    deal = Deal(title="Test Deal", value=15000, stage="new", companyId=company.id)
    session.add(deal)
    session.commit()
    session.refresh(deal)
    
    service = DealService(session)
    retrieved_deal = service.get(deal.id)
    assert retrieved_deal.id == deal.id
    assert retrieved_deal.title == "Test Deal"


def test_deal_service_get_deal_not_found(session):
    """Test getting a deal that doesn't exist"""
    service = DealService(session)
    result = service.get("non-existent-id")
    assert result is None


def test_deal_service_create_deal(session):
    """Test creating a deal through the service"""
    # Create a company first
    company = Company(name="Test Company Create", website="https://testcreate.com")
    session.add(company)
    session.commit()
    session.refresh(company)
    
    service = DealService(session)
    deal_data = {
        "title": "New Deal",
        "value": 25000,
        "stage": "new",
        "companyId": company.id
    }
    
    deal = service.create(deal_data)
    assert deal.title == "New Deal"
    assert deal.value == 25000
    assert deal.companyId == company.id
    assert deal.id is not None


def test_deal_service_update_deal(session):
    """Test updating a deal through the service"""
    # Create a company first
    company = Company(name="Test Company Update", website="https://testupdate.com")
    session.add(company)
    session.commit()
    session.refresh(company)
    
    # Create a deal
    deal = Deal(title="Original Deal", value=10000, stage="new", companyId=company.id)
    session.add(deal)
    session.commit()
    session.refresh(deal)
    
    service = DealService(session)
    update_data = {"title": "Updated Deal", "value": 30000, "stage": "proposal"}
    
    updated_deal = service.update(deal, update_data)
    assert updated_deal.title == "Updated Deal"
    assert updated_deal.value == 30000
    assert updated_deal.stage == "proposal"


def test_deal_service_delete_deal(session):
    """Test deleting a deal through the service"""
    # Create a company first
    company = Company(name="Test Company Delete", website="https://testdelete.com")
    session.add(company)
    session.commit()
    session.refresh(company)
    
    # Create a deal
    deal = Deal(title="Delete Me", value=5000, stage="new", companyId=company.id)
    session.add(deal)
    session.commit()
    session.refresh(deal)
    
    service = DealService(session)
    service.delete(deal)
    
    # Verify it's deleted
    result = service.get(deal.id)
    assert result is None 