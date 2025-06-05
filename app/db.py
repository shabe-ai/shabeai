from sqlmodel import SQLModel, create_engine, Session
import os
from sqlalchemy import text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///crm.db",          # fallback for local dev
)

# 👇 switch echo=False to True if you want verbose SQL logs
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Initialize the database, creating all tables if they don't exist."""
    SQLModel.metadata.create_all(engine)  # Only create if missing

def get_session() -> Session:
    return Session(engine)
