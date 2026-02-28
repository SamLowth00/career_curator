from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db import get_async_session
from app.auth.models import User
from app.models import UserSkill
from app.schemas import UserSkillCreate, UserSkillUpdate, UserSkillResponse
from app.auth.routes import current_active_user as get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[UserSkillResponse])
async def list_user_skills(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(select(UserSkill).where(UserSkill.user_id == user.id))
    return result.scalars().all()


@router.post("/", response_model=UserSkillResponse)
async def create_user_skill(
    skill: UserSkillCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_active_user),
):
    new_skill = UserSkill(
        user_id=user.id,
        name=skill.name,
        description=skill.description,
        level=skill.level,
    )
    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)
    return new_skill


@router.put("/{skill_id}", response_model=UserSkillResponse)
async def update_user_skill(
    skill_id: str,
    updates: UserSkillUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(UserSkill).where(
            (UserSkill.id == skill_id) & (UserSkill.user_id == user.id)
        )
    )
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    if updates.name is not None:
        skill.name = updates.name
    if updates.description is not None:
        skill.description = updates.description
    if updates.level is not None:
        skill.level = updates.level

    await db.commit()
    await db.refresh(skill)
    return skill


@router.delete("/{skill_id}")
async def delete_user_skill(
    skill_id: str,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(UserSkill).where(
            (UserSkill.id == skill_id) & (UserSkill.user_id == user.id)
        )
    )
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    await db.delete(skill)
    await db.commit()
    return None
