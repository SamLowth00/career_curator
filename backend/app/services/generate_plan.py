
from app.services.generate_work_plan import generate_work_plan
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.models import Job, Skill, JobSkill, Plan, PlanJob, UserSkill
from sqlalchemy import select, func
async def generate_plan(db: AsyncSession, user: User):

    # 1. Query skills with mention counts (how many jobs require each skill)
    skill_query = (
        select(Skill.name, func.count(JobSkill.job_id).label("mention_count"))
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .join(Job, JobSkill.job_id == Job.id)
        .where(Job.user_id == user.id)
        .group_by(Skill.id, Skill.name)
        .order_by(func.count(JobSkill.job_id).desc())
    )
    skill_result = await db.execute(skill_query)
    skill_rows = skill_result.all()

    skills_with_counts = [(row.name, row.mention_count) for row in skill_rows]

    # Distinct job IDs for PlanJob linking
    job_id_query = (
        select(Job.id)
        .join(JobSkill, Job.id == JobSkill.job_id)
        .join(Skill, JobSkill.skill_id == Skill.id)
        .where(Job.user_id == user.id)
        .distinct()
    )
    job_id_result = await db.execute(job_id_query)
    job_ids = [row[0] for row in job_id_result.all()]

    # 2. Fetch the user's existing skills for personalisation context
    user_skills_result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == user.id)
    )
    user_skill_rows = user_skills_result.scalars().all()
    user_skill_context = [
        {"name": s.name, "description": s.description, "level": s.level}
        for s in user_skill_rows
    ]

    # 3. Generate the plan text
    plan_content = generate_work_plan(skills_with_counts, user_skill_context)

    # 4. Delete existing plan for this user (PlanJob rows cascade automatically)
    existing = await db.execute(select(Plan).where(Plan.user_id == user.id))
    old_plan = existing.scalar_one_or_none()
    if old_plan:
        await db.delete(old_plan)
        await db.flush()  # make sure the delete is processed before inserting

    # 5. Save new Plan row
    new_plan = Plan(user_id=user.id, content=plan_content)
    db.add(new_plan)
    await db.flush()  # needed so new_plan.id is available for PlanJob

    # 6. Save PlanJob rows (one per job used)
    for job_id in job_ids:
        db.add(PlanJob(plan_id=new_plan.id, job_id=job_id))
    
    await db.commit()
    return plan_content


