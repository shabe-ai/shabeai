import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlmodel import Session

from .database import get_session
from .models import User

# Simple JWT settings
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_current_user(credentials=None, db=None):
    if credentials is None:
        credentials = Depends(security)
    if db is None:
        db = Depends(get_session)
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as err:
        raise HTTPException(status_code=401, detail="Invalid credentials") from err

def create_demo_user(db: Session):
    """Create the demo user if it doesn't exist."""
    user = User(
        id=str(uuid.uuid4()),
        email="demo@example.com",
        hashed_password=get_password_hash("demodemo"),
        is_active=True,
        is_superuser=False,
        is_verified=True,
        full_name="Demo User",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 