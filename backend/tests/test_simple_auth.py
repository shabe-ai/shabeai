from unittest.mock import patch

import jwt

from app.simple_auth import (
    create_access_token,
    create_demo_user,
    get_password_hash,
    verify_password,
)


def test_verify_password():
    """Test password verification"""
    # Test with correct password
    hashed = get_password_hash("testpass123")
    assert verify_password("testpass123", hashed) is True
    
    # Test with incorrect password
    assert verify_password("wrongpass", hashed) is False


def test_get_password_hash():
    """Test password hashing"""
    password = "testpass123"
    hashed = get_password_hash(password)
    
    # Should not be the same as original password
    assert hashed != password
    
    # Should be a string
    assert isinstance(hashed, str)
    
    # Should be different each time (due to salt)
    assert get_password_hash(password) != hashed


def test_create_access_token():
    data = {"sub": "user-id-123"}
    token = create_access_token(data)
    assert isinstance(token, str)
    decoded = jwt.decode(token, "your-secret-key-here", algorithms=["HS256"])
    assert decoded["sub"] == "user-id-123"
    assert "exp" in decoded


def test_create_demo_user(tmp_path):
    class DummyDB:
        def __init__(self):
            self.users = []
        def add(self, user):
            self.users.append(user)
        def commit(self):
            pass
        def refresh(self, user):
            pass
        def exec(self, query):
            # Mock the query result - return None to simulate no existing user
            class MockResult:
                def first(self):
                    return None
            return MockResult()
    
    db = DummyDB()
    user = create_demo_user(db)
    assert user.email == "demo@example.com"
    assert user.full_name == "Demo User"
    assert user.is_active
    assert user.is_verified
    assert user in db.users

# get_current_user is best tested via integration, not unit, due to Depends and JWT

@patch('app.simple_auth.get_current_user')
def test_get_current_user_mock(mock_get_current_user):
    """Test get_current_user with mock"""
    # This is a placeholder test since get_current_user depends on FastAPI context
    # In a real test, you'd need to set up the proper FastAPI context
    pass 