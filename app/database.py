from sqlmodel import SQLModel, create_engine, Session
import os

# Neon PostgreSQL connection string
DATABASE_URL = "postgresql://neondb_owner:npg_wsArWxq1MQX4@ep-wispy-credit-a89k7lm0-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_size=5,  # Maximum number of connections to keep
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
)

def init_db():
    """Initialize the database, creating all tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    """Get a new database session."""
    return Session(engine) 