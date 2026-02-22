from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_async_session
from app.auth.models import User
from app.auth.routes import current_active_user as get_current_active_user
from app.services.generate_plan import generate_plan
from app.models import Plan

router = APIRouter()

@router.post('/generate-plan')
async def generate_new_plan(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    result = await generate_plan(db, user)

    return result

@router.get('/saved-plan')
async def get_saved_plan(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    result = await db.execute(select(Plan).where(Plan.user_id == user.id))
    plan = result.scalar_one_or_none()
    
    if plan:
        return plan.content
    return None