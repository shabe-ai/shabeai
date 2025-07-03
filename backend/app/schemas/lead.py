from pydantic import BaseModel


class LeadBase(BaseModel):
    email: str
    firstName: str
    lastName: str
    phone: str | None = None
    companyId: str | None = None

class LeadCreate(LeadBase):
    pass

class LeadOut(LeadBase):
    id: str

    class Config:
        from_attributes = True 