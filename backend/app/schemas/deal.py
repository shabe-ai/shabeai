from pydantic import BaseModel

class DealBase(BaseModel):
    title: str
    value: int
    stage: str = "new"
    companyId: str

class DealCreate(DealBase):
    pass

class DealOut(DealBase):
    id: str

    class Config:
        from_attributes = True 