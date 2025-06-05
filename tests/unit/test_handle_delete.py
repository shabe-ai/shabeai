from app.commands import handle
from app.models import Account, Lead
from app.database import get_session, init_db
from app.utils import to_uuid
import uuid

def ctx():
    """Create a dummy context with a random user ID."""
    return {"id": str(uuid.uuid4())}

def setup_account(session, name: str, user_id: str) -> Account:
    """Create and commit an account for testing."""
    acc = Account(name=name, user_id=to_uuid(user_id))
    session.add(acc)
    session.commit()
    return acc

def test_delete_account_with_leads():
    """Test that we can't delete an account with attached leads."""
    init_db()  # Ensure tables exist
    user = str(uuid.uuid4())
    with get_session() as s:
        acc = setup_account(s, "globex", user)
        s.add(Lead(email="x@globex.com", account_id=acc.id, user_id=to_uuid(user)))
        s.commit()
    
    # Should refuse to delete account with leads
    res = handle("delete account globex", {"id": user})
    assert "delete them first" in res.lower()

def test_delete_account_empty():
    """Test that we can delete an account with no leads."""
    init_db()  # Ensure tables exist
    user = str(uuid.uuid4())
    with get_session() as s:
        acc = setup_account(s, "empty", user)
    
    # Should allow deletion of empty account
    res = handle("delete account empty", {"id": user})
    assert "deleted" in res.lower() 