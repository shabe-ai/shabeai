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
        company = Company(**company_in.model_dump())
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def update(self, db_company, company_update):
        for k, v in company_update.model_dump(exclude_unset=True).items():
            setattr(db_company, k, v)
        self.session.add(db_company)
        self.session.commit()
        self.session.refresh(db_company)
        return db_company

    def delete(self, db_company):
        self.session.delete(db_company)
        self.session.commit() 