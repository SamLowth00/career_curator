
from app.langchain.generate_work_plan import generate_work_plan
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.models import Job, Skill, JobSkill, Plan, PlanJob
from sqlalchemy import select, distinct
async def generate_plan(db: AsyncSession, user: User):

    # 1. Query skills AND their source job IDs together
    query = (
        select(Skill, Job.id.label("job_id"))
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .join(Job, JobSkill.job_id == Job.id)
        .where(Job.user_id == user.id)
        .distinct()
    )
    result = await db.execute(query)
    rows = result.all()

    skill_names = list({row.Skill.name for row in rows})   # deduplicate
    job_ids = list({row.job_id for row in rows})           # unique job IDs

    # 2. Generate the plan text
    plan_content = generate_work_plan(skill_names)

    # 3. Delete existing plan for this user (PlanJob rows cascade automatically)
    existing = await db.execute(select(Plan).where(Plan.user_id == user.id))
    old_plan = existing.scalar_one_or_none()
    if old_plan:
        await db.delete(old_plan)
        await db.flush()  # make sure the delete is processed before inserting

    # 4. Save new Plan row
    new_plan = Plan(user_id=user.id, content=plan_content)
    db.add(new_plan)
    await db.flush()  # needed so new_plan.id is available for PlanJob

    # 5. Save PlanJob rows (one per job used)
    for job_id in job_ids:
        db.add(PlanJob(plan_id=new_plan.id, job_id=job_id))
    
    await db.commit()
    return plan_content


