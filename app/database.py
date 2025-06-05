import os, sys
from sqlmodel import SQLModel, create_engine, Session

TESTING = "pytest" in sys.modules              # <─ detects pytest
DATABASE_URL = (
    "sqlite:///:memory:"                       # tests: fast, throw-away DB
    if TESTING
    else os.getenv("DATABASE_URL", "sqlite:///crm.db")
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False},  # lets Starlette TestClient share it
)

def init_db() -> None:
    """Initialize the database, creating all tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session 