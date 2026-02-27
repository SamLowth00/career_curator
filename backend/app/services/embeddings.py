from openai import AsyncOpenAI
from app.models import Job
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

async def generate_embedding(text: str) -> list[float]:
    client = AsyncOpenAI()
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    print(f"embedding: {response.data}")
    return response.data[0].embedding



async def get_similar_jobs(db: AsyncSession, user_id: uuid.UUID, query_embedding: list[float], top_k: int = 3) -> list[Job]:
    result = await db.execute(
        select(Job)
        .where(Job.user_id == user_id)
        .where(Job.embedding.isnot(None))
        .order_by(Job.embedding.cosine_distance(query_embedding))
        .limit(top_k)
    )
    return result.scalars().all()