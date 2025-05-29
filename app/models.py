from sqlmodel import SQLModel, Field, Relationship
import datetime

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    leads: list["Lead"] = Relationship(back_populates="account")

class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    created_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow
    )

    account_id: int | None = Field(default=None, foreign_key="account.id")
    account: Account | None = Relationship(back_populates="leads")
