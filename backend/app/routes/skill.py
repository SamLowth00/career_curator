from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.auth.models import User
from app.auth.routes import current_active_user as get_current_active_user
from app.services.fetch_user_skills import fetch_user_skills
from app.models import Skill
from typing import List
router = APIRouter()

@router.post('/list')
async def fetch_skills(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    skillReturned = await fetch_user_skills(db, user)
    return skillReturned