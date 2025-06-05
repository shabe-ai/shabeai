from functools import wraps
from typing import Callable
from app.db import get_session
from app.models import AuditLog

def audit(action: str):
    """Decorator to capture before/after states."""
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            before_state = kwargs.get("before")  # optional
            result, after_state = fn(*args, **kwargs)
            email = after_state.get("email") or before_state.get("email")
            with get_session() as s:
                s.add(
                    AuditLog(
                        email=email,
                        action=action,
                        before=before_state,
                        after=after_state,
                    )
                )
                s.commit()
            return result
        return wrapper
    return decorator 