from .database import get_session
from .simple_auth import get_current_user


def get_db():
    """Get database session dependency"""
    yield from get_session()


def get_current_active_user():
    """Get current active user dependency"""
    return get_current_user
