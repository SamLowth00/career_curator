from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.auth.models import User
from app.auth.routes import current_active_user as get_current_active_user
from app.models import Job, Skill, JobSkill
from app.schemas import SalarySummary
from sqlalchemy import select, func

router = APIRouter()

@router.get('/average', response_model=SalarySummary)
async def average_salary(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
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
    print(f'salaryy {salary_data.avg_salary}')
    return salary_data

    