from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.auth.models import User
from app.auth.routes import current_active_user as get_current_active_user
from app.services.generate_plan import generate_plan
router = APIRouter()

@router.post('/generate-plan')
async def generate_new_plan(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    result = await generate_plan(db, user)

    return result
