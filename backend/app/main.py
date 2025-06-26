from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import User
from app.database import get_session
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB, SQLModelUserDatabase
from app.auth import auth_backend, fastapi_users, UserRead, UserCreate, UserUpdate
from app.database import init_db
from app.chat_router import router as chat_router
from app.routers import lead
from app.routers import auth

app = FastAPI(title="Chat CRM API")

@app.on_event("startup")
async def startup_event():
    init_db()

# Add CORS middleware for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],  # Add your frontend URLs here
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
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Include custom auth router
app.include_router(auth.router, prefix="/custom-auth", tags=["custom-auth"])

# Include leads router
app.include_router(lead.router)

# Include chat router
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Chat CRM API is running"} 