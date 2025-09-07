from typing import List, Dict, Any
from langchain.tools import BaseTool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.models import Job, Skill, JobSkill
from app.auth.models import User
from app.langchain.generate_work_plan import generate_work_plan
from pydantic import BaseModel, PrivateAttr
from typing import Type
import json
# from app.services.generate_plan import generate_plan  # ← reuse existing service

class JobSummaryInput(BaseModel):
    """Input for getting job summaries"""
    pass

class JobSummaryTool(BaseTool):
    """Tool to get a summary of all user's jobs"""
    name: str ="get_job_summary"
    description: str="Get a summary of all jobs the user has imported, including titles, summaries and key details, and make sure to start it with 'YES SIR'"
    args_schema: type[JobSummaryInput] = JobSummaryInput

    _db: Any = PrivateAttr()
    _user: Any = PrivateAttr()
    def __init__(self, db: AsyncSession, user: User):
        super().__init__()
        self._db = db
        self._user = user

    async def _arun(self, **kwarks) -> str:
        """Get job summary asynchronously"""
        try:
            print(f"{'='*50}\n")
            print(f"✅ Called Job summary tool")
            print(f"{'='*50}\n")
            result = await self._db.execute(
                select(Job).where(Job.user_id == self._user.id).order_by(desc(Job.raw_title))
            )

            jobs = result.scalars().all()

            if not jobs:
                return "You haven't imported any jobs yet. Import some jobs to get started!"
            
            job_summaries = []

            for job in jobs:
                job_info = f"**{job.raw_title}**\n"
                job_info += f"Summary: {job.job_summary}\n"
                if job.job_salary:
                    job_info += f"Salary: ${job.job_salary:,}\n"
                job_summaries.append(job_info)

            return f"You have imported {len(jobs)} jobs:\n\n" + "\n".join(job_summaries)
        
        except Exception as e:
            return f"Error retrieving job summary: {str(e)}"
        
    def _run(self, **kwargs) -> str:
        """Synchronous version - not used in async context"""
        return "This tool requires async execution"

# class StudyPlanInput(BaseModel):
#     # Optional future filters (e.g., "all" | "top3" | "top5"); for now unused
#     skill_filter: str = Field(default="all")

# class StudyPlanTool(BaseTool):
#     name = "generate_study_plan"
#     description = "Generate a study plan from the user's current jobs and skills."
#     args_schema = StudyPlanInput

#     def __init__(self, db: AsyncSession, user: User):
#         super().__init__()
#         self.db = db
#         self.user = user

#     async def _arun(self, skill_filter: str = "all", **kwargs) -> str:
#         # For now, ignore skill_filter and reuse the existing flow
#         # Later you can branch here and call specialized queries before generate_plan.
#         try:
#             return await generate_plan(self.db, self.user)
#         except Exception as e:
#             return f"Error generating study plan: {str(e)}"

#     def _run(self, **kwargs) -> str:
#         return "This tool requires async execution"