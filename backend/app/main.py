from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import UserCreate, UserRead, UserUpdate, auth_backend, fastapi_users
from app.chat_router import router as chat_router
from app.database import init_db
from app.logging_config import setup_logging
from app.middleware.request_id import RequestIDMiddleware
from app.routers import auth, lead, meta

# Setup structured logging
setup_logging()

app = FastAPI(title="Chat CRM API")


@app.on_event("startup")
async def startup_event():
    init_db()


# Add Request ID middleware first (before everything else)
app.add_middleware(RequestIDMiddleware)

# Add CORS middleware for local frontend
origins = ["http://localhost:3001"]  # Next dev URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

# Include meta router for health and version endpoints
app.include_router(meta.router)


@app.get("/")
async def root():
    return {"message": "Chat CRM API is running"}
