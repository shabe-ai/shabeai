import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

def init_db() -> None:
    """Create tables once (no-op if they already exist)."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Yield a Session; make sure tables exist."""
    init_db()
    with Session(engine) as session:
        yield session 