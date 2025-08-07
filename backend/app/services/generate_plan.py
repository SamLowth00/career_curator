
from app.langchain.generate_work_plan import generate_work_plan
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.models import Job, Skill, JobSkill
from sqlalchemy import select, distinct
async def generate_plan(db: AsyncSession, user: User):
    query = (
        select(Skill)
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .join(Job, JobSkill.job_id == Job.id)
        .distinct()
    )
    result = await db.execute(query)
    skills = result.scalars().all()
    
    # Extract just the skill names into a list
    skill_names = [skill.name for skill in skills]
    resp = generate_work_plan(skill_names)
    return resp


