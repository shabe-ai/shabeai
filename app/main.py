from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import User
from app.db import get_session
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB, SQLModelUserDatabase
from app.auth import auth_backend, fastapi_users
from app.database import init_db
from app.schemas import UserRead, UserCreate  # Import the schemas

app = FastAPI(title="Chat CRM API")

@app.on_event("startup")
async def startup_event():
    init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include FastAPI Users routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(
        user_schema=UserRead,
        user_create_schema=UserCreate,
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)

@app.get("/")
async def root():
    return {"message": "Chat CRM API is running"} 