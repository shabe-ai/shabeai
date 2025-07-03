from sqlmodel import Session, select

from ..models import Deal


class DealService:
    def __init__(self, session: Session):
        self.session = session

    def list(self):
        return self.session.exec(select(Deal)).all()

    def get(self, deal_id: str):
        return self.session.get(Deal, deal_id)

    def create(self, deal_in):
        # Handle both Pydantic v1 and v2
        if hasattr(deal_in, "model_dump"):
            deal_data = deal_in.model_dump()
        elif hasattr(deal_in, "dict"):
            deal_data = deal_in.dict()
        else:
            deal_data = dict(deal_in)
        deal = Deal(**deal_data)
        self.session.add(deal)
        self.session.commit()
        self.session.refresh(deal)
        return deal

    def update(self, db_deal, deal_update):
        # Handle both Pydantic v1 and v2
        if hasattr(deal_update, "model_dump"):
            update_data = deal_update.model_dump(exclude_unset=True)
        elif hasattr(deal_update, "dict"):
            update_data = deal_update.dict(exclude_unset=True)
        else:
            update_data = dict(deal_update)
        for k, v in update_data.items():
            setattr(db_deal, k, v)
        self.session.add(db_deal)
        self.session.commit()
        self.session.refresh(db_deal)
        return db_deal

    def delete(self, db_deal):
        self.session.delete(db_deal)
        self.session.commit()
