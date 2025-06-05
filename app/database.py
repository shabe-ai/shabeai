import os, sys
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager

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
    connect_args={"check_same_thread": False} if TESTING else {},  # lets Starlette TestClient share it
)

def init_db() -> None:
    """Create tables once (no-op if they already exist)."""
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    """Yield a Session; make sure tables exist (helps unit-tests)."""
    init_db()                      # <-- NEW line
    with Session(engine) as session:
        yield session 