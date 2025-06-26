from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional, List
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("email"),)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    full_name: str | None = None

class Company(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(unique=True)
    website: Optional[str] = None
    linkedinUrl: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    leads: List["Lead"] = Relationship(back_populates="company")
    deals: List["Deal"] = Relationship(back_populates="company")

class Lead(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True)
    firstName: str
    lastName: str
    phone: Optional[str] = None
    linkedinUrl: Optional[str] = None
    companyId: Optional[str] = Field(default=None, foreign_key="company.id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    company: Optional[Company] = Relationship(back_populates="leads")
    tasks: List["Task"] = Relationship(back_populates="lead")

class Deal(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    value: int
    stage: str = Field(default="new")
    companyId: str = Field(foreign_key="company.id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    company: Company = Relationship(back_populates="deals")

class Task(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    dueDate: datetime
    isDone: bool = Field(default=False)
    leadId: Optional[str] = Field(default=None, foreign_key="lead.id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    lead: Optional[Lead] = Relationship(back_populates="tasks") 