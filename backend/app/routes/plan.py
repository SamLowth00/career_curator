from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db import get_async_session
from app.auth.models import User
from app.auth.routes import current_active_user as get_current_active_user
from app.services.generate_plan import generate_plan
from app.models import Plan, PlanJob

router = APIRouter()

@router.post('/generate-plan')
async def generate_new_plan(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    result = await generate_plan(db, user)

    return result

@router.get('/saved-plan')
async def get_saved_plan(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    result = await db.execute(
        select(Plan, func.count(PlanJob.id).label("job_count"))
        .outerjoin(PlanJob, PlanJob.plan_id == Plan.id)
        .where(Plan.user_id == user.id)
        .group_by(Plan.id)
    )

    row = result.one_or_none()
    if row:
        return { 'content': row.Plan.content, 'job_count': row.job_count }
    return None