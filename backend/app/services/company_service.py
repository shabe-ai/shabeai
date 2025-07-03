from sqlmodel import Session, select

from ..models import Company


class CompanyService:
    def __init__(self, session: Session):
        self.session = session

    def list(self):
        return self.session.exec(select(Company)).all()

    def get(self, company_id: str):
        return self.session.get(Company, company_id)

    def create(self, company_in):
        # Handle both Pydantic v1 and v2
        if hasattr(company_in, "model_dump"):
            company_data = company_in.model_dump()
        elif hasattr(company_in, "dict"):
            company_data = company_in.dict()
        else:
            company_data = dict(company_in)
        company = Company(**company_data)
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def update(self, db_company, company_update):
        # Handle both Pydantic v1 and v2
        if hasattr(company_update, "model_dump"):
            update_data = company_update.model_dump(exclude_unset=True)
        elif hasattr(company_update, "dict"):
            update_data = company_update.dict(exclude_unset=True)
        else:
            update_data = dict(company_update)
        for k, v in update_data.items():
            setattr(db_company, k, v)
        self.session.add(db_company)
        self.session.commit()
        self.session.refresh(db_company)
        return db_company

    def delete(self, db_company):
        self.session.delete(db_company)
        self.session.commit()
