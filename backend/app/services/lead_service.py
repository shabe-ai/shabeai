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
        # Handle both Pydantic v1 and v2
        if hasattr(lead_in, 'model_dump'):
            lead_data = lead_in.model_dump()
        elif hasattr(lead_in, 'dict'):
            lead_data = lead_in.dict()
        else:
            lead_data = dict(lead_in)
        lead = Lead(**lead_data)
        self.session.add(lead)
        self.session.commit()
        self.session.refresh(lead)
        return lead

    def update(self, db_lead, lead_update):
        # Handle both Pydantic v1 and v2
        if hasattr(lead_update, 'model_dump'):
            update_data = lead_update.model_dump(exclude_unset=True)
        elif hasattr(lead_update, 'dict'):
            update_data = lead_update.dict(exclude_unset=True)
        else:
            update_data = dict(lead_update)
        for k, v in update_data.items():
            setattr(db_lead, k, v)
        self.session.add(db_lead)
        self.session.commit()
        self.session.refresh(db_lead)
        return db_lead

    def delete(self, db_lead):
        self.session.delete(db_lead)
        self.session.commit()
