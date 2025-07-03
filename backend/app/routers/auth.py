from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import select

from ..database import get_session
from ..models import User
from ..simple_auth import (
    create_access_token,
    create_demo_user,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db=Depends(get_session)) -> Token:
    user = db.exec(select(User).where(User.email == user_credentials.email)).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=Token)
def register(user_data: UserRegister, db=Depends(get_session)) -> Token:
    # Check if user already exists
    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.id})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/setup-demo")
def setup_demo(db=Depends(get_session)) -> dict[str, str]:
    """Setup demo user for testing."""
    create_demo_user(db)
    return {"message": "Demo user setup complete"}


@router.get("/users", response_model=list[User])
def list_users(db=Depends(get_session)) -> list[User]:
    return db.query(User).all()
