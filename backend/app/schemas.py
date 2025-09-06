from typing import Optional
from pydantic import BaseModel
from uuid import UUID
# --- Job Schemas ---

class JobCreate(BaseModel):
    raw_title: str
    raw_description: str
    job_salary: Optional[int] = None
    link: Optional[str] = None

class JobResponse(BaseModel):
    id: UUID
    job_summary: str
    raw_title: str
    raw_description: str
    job_salary: Optional[int] = None
    link: Optional[str] = None
    class Config:
        orm_mode = True

# --- Skill Schemas ---

class SkillCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SkillResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class JobSkillBase(BaseModel):
    job_id: UUID
    skill_id: UUID

class JobSkillCreate(JobSkillBase):
    pass

class JobSkillRead(JobSkillBase):
    id: UUID

    class Config:
        orm_mode = True

class SalarySummary(BaseModel):
    avg_salary: Optional[float] = None
    records_used: int = 0