from sqlmodel import Session
from faker import Faker
from app.models import Company, Lead, Deal, Task

# Initialize Faker for test data generation
fake = Faker()

class LeadFactory:
    """Factory for creating Lead test data."""
    
    @staticmethod
    def create(**kwargs) -> dict:
        """Create a lead payload with default values."""
        defaults = {
            "email": fake.email(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "phone": fake.phone_number(),
            "linkedinUrl": fake.url(),
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create_model(session: Session, **kwargs) -> Lead:
        """Create and save a Lead model to the database."""
        lead_data = LeadFactory.create(**kwargs)
        lead = Lead(**lead_data)
        session.add(lead)
        session.commit()
        session.refresh(lead)
        return lead

class CompanyFactory:
    """Factory for creating Company test data."""
    
    @staticmethod
    def create(**kwargs) -> dict:
        """Create a company payload with default values."""
        defaults = {
            "name": fake.company(),
            "website": fake.url(),
            "linkedinUrl": fake.url(),
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create_model(session: Session, **kwargs) -> Company:
        """Create and save a Company model to the database."""
        company_data = CompanyFactory.create(**kwargs)
        company = Company(**company_data)
        session.add(company)
        session.commit()
        session.refresh(company)
        return company

class DealFactory:
    """Factory for creating Deal test data."""
    
    @staticmethod
    def create(company_id: str, **kwargs) -> dict:
        """Create a deal payload with default values."""
        defaults = {
            "title": fake.catch_phrase(),
            "value": fake.random_int(min=1000, max=100000),
            "stage": fake.random_element(["new", "qualified", "proposal", "negotiation", "won", "lost"]),
            "companyId": company_id,
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create_model(session: Session, company_id: str, **kwargs) -> Deal:
        """Create and save a Deal model to the database."""
        deal_data = DealFactory.create(company_id, **kwargs)
        deal = Deal(**deal_data)
        session.add(deal)
        session.commit()
        session.refresh(deal)
        return deal

class TaskFactory:
    """Factory for creating Task test data."""
    
    @staticmethod
    def create(lead_id: str = None, **kwargs) -> dict:
        """Create a task payload with default values."""
        defaults = {
            "title": fake.sentence(nb_words=4),
            "dueDate": fake.future_datetime(),
            "isDone": False,
            "leadId": lead_id,
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create_model(session: Session, lead_id: str = None, **kwargs) -> Task:
        """Create and save a Task model to the database."""
        task_data = TaskFactory.create(lead_id, **kwargs)
        task = Task(**task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

# Test data constants
valid_lead_payload = LeadFactory.create()
valid_company_payload = CompanyFactory.create()
valid_deal_payload = DealFactory.create(company_id="test-company-id")
valid_task_payload = TaskFactory.create() 