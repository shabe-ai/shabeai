from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    dueDate: datetime
    isDone: bool = False
    leadId: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: str

    class Config:
        from_attributes = True 