# app/auth/manager.py
from fastapi_users.manager import BaseUserManager
from app.auth.models import User
from app.db import async_session
from uuid import UUID
import uuid
import os

SECRET = os.getenv("JWT_SECRET_KEY")

class UserManager(BaseUserManager[User, uuid.UUID]):
    user_db_model = User
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"User registered: {user.id}")
    
    def parse_id(self, value: str) -> UUID:
        return UUID(value)