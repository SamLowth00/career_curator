from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.auth.models import User
from app.auth.routes import current_active_user as get_current_active_user
from app.models import Job, Skill, JobSkill
from app.schemas import SalarySummary
from sqlalchemy import select, func
from app.cache import cache_key, get_cached, set_cached
import time

router = APIRouter()

@router.get('/average', response_model=SalarySummary)
async def average_salary(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    start_s = time.perf_counter()
    # check cache first
    key = cache_key("salary:avg", str(user.id))
    cached = await get_cached(key)
    if cached:
        elapsed_s = time.perf_counter() - start_s
        print(f"📦 Ave salary Cache hit time: {elapsed_s:.6f}s")
        return SalarySummary(**cached)

    # if not cached, get from database
    query = (
        select(func.avg(Job.job_salary).label('avgSalary'), func.count(Job.job_salary).label('recordsUsed'))
        .where(Job.user_id == user.id and Job.job_salary.isnot(None))
    )

    result = await db.execute(query)
    salary_return = result.first()

    salary_data = SalarySummary(
        avg_salary=round(salary_return.avgSalary, 2),
        records_used=salary_return.recordsUsed
    )

    # set cache
    await set_cached(key, salary_data.model_dump())

    elapsed_s = time.perf_counter() - start_s
    print(f"❌ Ave salary Cache Miss {elapsed_s:.6f}s")
    return salary_data

    