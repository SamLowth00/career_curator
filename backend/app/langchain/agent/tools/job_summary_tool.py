from typing import Any
from langchain.tools import BaseTool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import Job
from app.auth.models import User
from pydantic import BaseModel, PrivateAttr
from app.services.embeddings import get_similar_jobs, generate_embedding

class JobSummaryInput(BaseModel):
    """Input for getting job summaries"""
    user_query: str
    pass


class JobSummaryTool(BaseTool):
    """Tool to get a summary of all user's jobs"""
    name: str = "get_job_summary"
    description: str = (
        "Search for the most relevant jobs based on a topic or question. "
        "Use this whenever the user asks about specific skills, roles, salaries, or job types. "
        "Prefer this over asking for all jobs."
    )
    args_schema: type[JobSummaryInput] = JobSummaryInput

    _db: Any = PrivateAttr()
    _user: Any = PrivateAttr()

    def __init__(self, db: AsyncSession, user: User):
        super().__init__()
        self._db = db
        self._user = user

    async def _arun(self, user_query: str) -> str:
        """Get job summary asynchronously"""
        try:

            query_embedding = await generate_embedding(user_query)
            semantic_similar_jobs = await get_similar_jobs(self._db, self._user.id, query_embedding, top_k=3)

            if not semantic_similar_jobs:
                return "You haven't imported any jobs yet. Import some jobs to get started!"

            job_summaries = []

            for job in semantic_similar_jobs:
                job_info = f"**{job.raw_title}**\n"
                job_info += f"Summary: {job.job_summary}\n"
                if job.job_salary:
                    job_info += f"Salary: ${job.job_salary:,}\n"
                job_summaries.append(job_info)

            return f"Most relevant jobs:\n\n" + "\n".join(job_summaries)

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
