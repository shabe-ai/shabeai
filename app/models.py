from sqlmodel import SQLModel, Field, Relationship
import datetime
import enum
from typing import Any, Optional, List
from sqlalchemy import Column
from sqlalchemy.types import JSON
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import UniqueConstraint
import uuid
from app.database import get_session

class Stage(str, enum.Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    WON = "won"
    LOST = "lost"

class User(SQLModelBaseUserDB, table=True):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("email"),)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    full_name: str | None = None

    # Relationships
    accounts: List["Account"] = Relationship(back_populates="user")
    leads: List["Lead"] = Relationship(back_populates="user")

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    created_at: datetime.datetime | None = Field(default_factory=datetime.datetime.utcnow)
    
    user_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="user.id",
        index=True,
    )
    user: User | None = Relationship(back_populates="accounts")

    leads: List["Lead"] = Relationship(back_populates="account")

class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    created_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow
    )

    account_id: int | None = Field(default=None, foreign_key="account.id")
    account: Account | None = Relationship(back_populates="leads")

    user_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="user.id",
        index=True,
    )
    user: User | None = Relationship(back_populates="leads")

    tags: str | None = Field(default="", nullable=False)
    stage: Stage = Field(default=Stage.NEW)

class AuditLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str                         # which lead changed (simplest key)
    action: str                        # "create", "update", "tag", "stage"
    before: dict[str, Any] | None = Field(sa_column=Column(JSON))
    after:  dict[str, Any] | None = Field(sa_column=Column(JSON))
    ts: datetime.datetime | None = Field(default_factory=datetime.datetime.utcnow)

def get_db():
    """Get a database session."""
    return get_session()
