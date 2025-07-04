from uuid import UUID

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers

from app.auth import UserCreate, UserRead, UserUpdate, auth_backend, get_user_manager
from app.chat_router import router as chat_router
from app.database import init_db
from app.logging_config import setup_logging
from app.middleware.request_id import RequestIDMiddleware
from app.models import User
from app.routers import auth, company, deal, lead, meta, task

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

# --------------------------------------------------------------------------- #
# FastAPI-Users setup                                                         #
# --------------------------------------------------------------------------- #

# Instantiate once so we can derive all feature routers from it.
fastapi_users: FastAPIUsers = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

# ------------------- Auth routes ------------------- #
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Include custom auth router
app.include_router(auth.router, prefix="/auth", tags=["custom-auth"])

# Include leads router
app.include_router(lead.router)

# Include company router
app.include_router(company.router)

# Include deal router
app.include_router(deal.router)

# Include task router
app.include_router(task.router)

# Include chat router
app.include_router(chat_router, prefix="/api", tags=["chat"])

# Include meta router for health and version endpoints
app.include_router(meta.router)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/")
async def root():
    return {"message": "Chat CRM API is running"}
