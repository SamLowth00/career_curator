from fastapi_users import schemas
from typing import Optional
from uuid import UUID

class UserRead(schemas.BaseUser[UUID]):
    first_name: Optional[str]
    last_name: Optional[str]

class UserCreate(schemas.BaseUserCreate):
    first_name: Optional[str]
    last_name: Optional[str]

class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
