from fastapi_users import schemas
from pydantic import EmailStr
import uuid

class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None

class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    full_name: str | None = None 