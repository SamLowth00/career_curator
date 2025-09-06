from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.auth.models import User
from app.models import Job, Skill, JobSkill
from typing import List

async def fetch_user_skills(db: AsyncSession, user: User):    
    query = (
        select(Skill.id, Skill.name, func.count(JobSkill.job_id).label('job_count'))
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .join(Job, JobSkill.job_id == Job.id)
        .where(Job.user_id == user.id)
        .group_by(Skill.id)
    )

    result = await db.execute(query)
    skills = result.mappings().all()

    print(f'{skills}')
    return skills


