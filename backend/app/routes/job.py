from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db import get_async_session
from app.auth.models import User
from app.models import Job, Skill, JobSkill
from app.schemas import JobCreate, JobResponse, JobImportRequest
from app.langchain.parse_job import parse_job_from_content
from app.auth.routes import current_active_user as get_current_active_user
from app.services.embeddings import generate_embedding
from app.services.import_job import parse_job
from app.cache import cache_key, invalidate
router = APIRouter()

@router.post("/import")
async def import_job_from_url(payload: JobImportRequest, user: User = Depends(get_current_active_user)):
    job = parse_job(payload.url)
    return job

@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    result = await db.execute(select(Skill).where(Skill.user_id == user.id))
    user_skills = result.scalars().all()
    user_skill_names = [skill.name for skill in user_skills]

    summary, required_skills = parse_job_from_content(job.raw_title, job.raw_description, user_skill_names)
    # 2. Get all skills in Skill table

    skill_name_map = {s.name.lower(): s for s in user_skills}
    # 3. Create Job record
    new_job = Job(
        user_id=user.id,
        job_summary=summary,
        job_salary=job.job_salary, 
        raw_title=job.raw_title,
        raw_description=job.raw_description,
        link=job.link
    )

    db.add(new_job)
    await db.flush()  # To get new_job.id

        # 4. For each required skill
    for skill_name in required_skills:
        skill = skill_name_map.get(skill_name.lower())
        if not skill:
            skill = Skill(name=skill_name, user_id=user.id)
            db.add(skill)
            await db.flush()
            skill_name_map[skill_name.lower()] = skill
        
        job_skill = JobSkill(job_id=new_job.id, skill_id=skill.id)
        db.add(job_skill)
    
    # 5. Generate embedding for the job summary
    text_to_embed = f"{job.raw_title}: {summary}"
    embedding = await generate_embedding(text_to_embed)
    new_job.embedding = embedding
    
    await db.commit()

    # invalidate cache for salary average
    invalidate(cache_key("salary:avg", str(user.id)))
    return new_job

@router.post("/backfill-embeddings")
async def backfill_embeddings(db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
    result = await db.execute(
        select(Job).where(Job.user_id == user.id).where(Job.embedding == None)
    )
    jobs_without_embeddings = result.scalars().all()

    print(f"🔧 Backfilling embeddings for {len(jobs_without_embeddings)} jobs")

    for job in jobs_without_embeddings:
        text_to_embed = f"{job.raw_title}: {job.job_summary}"
        job.embedding = await generate_embedding(text_to_embed)
        print(f"✅ Generated embedding for: {job.raw_title}")

    await db.commit()
    return {"backfilled": len(jobs_without_embeddings)}

@router.get("/", response_model=List[JobResponse])
async def get_jobs(user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Job).where(Job.user_id == user.id))
    user_jobs = result.scalars().all()
    return user_jobs

@router.delete("/{job_id}")
async def delete_job(job_id: str, db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_active_user)):
        # Fetch the job by ID and user
    result = await db.execute(
        select(Job).where((Job.id == job_id) & (Job.user_id == user.id))
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        # Get all skills associated with this job before deleting
    job_skills_result = await db.execute(
        select(JobSkill).where(JobSkill.job_id == job_id)
    )
    job_skills = job_skills_result.scalars().all()
    # Extract skill IDs that will be affected
    affected_skill_ids = [job_skill.skill_id for job_skill in job_skills]

    await db.delete(job)
    await db.commit()

    for skill_id in affected_skill_ids:
        # Check if this skill is still used by any other jobs from this user
        remaining_job_skills_result = await db.execute(
            select(JobSkill)
            .join(Job, JobSkill.job_id == Job.id)
            .where((JobSkill.skill_id == skill_id) & (Job.user_id == user.id))
        )
        #this gets any other jobskills from this user, that is from one of the deleted jobskills
        
        remaining_job_skills = remaining_job_skills_result.scalars().all()
        print(f'remaining jobs: {remaining_job_skills}')
        # If no other jobs use this skill, delete the skill
        if not remaining_job_skills:
            skill_result = await db.execute(
                select(Skill).where((Skill.id == skill_id) & (Skill.user_id == user.id))
            )
            skill = skill_result.scalar_one_or_none()
            print(f'skill: {skill}')
            if skill:
                await db.delete(skill)
    
    await db.commit()

    # invalidate cache for salary average
    await invalidate(cache_key("salary:avg", str(user.id)))


    return None  