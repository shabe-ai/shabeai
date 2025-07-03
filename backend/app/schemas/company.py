from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    website: str | None = None
    linkedinUrl: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyOut(CompanyBase):
    id: str

    class Config:
        from_attributes = True
