from sqlmodel import SQLModel, Field
import datetime

class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    created_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow
    )
