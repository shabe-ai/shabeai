from sqlmodel import Session, select

from ..models import Lead


class LeadService:
    def __init__(self, session: Session):
        self.session = session

    def list(self):
        return self.session.exec(select(Lead)).all()

    def get(self, lead_id: str):
        return self.session.get(Lead, lead_id)

    def create(self, lead_in):
        lead = Lead(**lead_in.model_dump())
        self.session.add(lead)
        self.session.commit()
        self.session.refresh(lead)
        return lead

    def update(self, db_lead, lead_update):
        for k, v in lead_update.model_dump(exclude_unset=True).items():
            setattr(db_lead, k, v)
        self.session.add(db_lead)
        self.session.commit()
        self.session.refresh(db_lead)
        return db_lead

    def delete(self, db_lead):
        self.session.delete(db_lead)
        self.session.commit()
