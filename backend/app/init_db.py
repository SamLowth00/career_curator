# app/init_db.py
import asyncio
from app.db import engine, Base
from app.auth.models import User
from app.models import Job, Skill, JobSkill

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())