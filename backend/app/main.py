from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import auth_router, register_router, users_router
from app.routes.job import router as job_router
from app.routes.plan import router as plan_router
from app.routes.skill import router as skill_router
from app.routes.salary import router as salary_router
from app.routes.chat import router as agent_router

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite dev server
    # Add more origins if needed
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,   # Required for cookies/auth
    allow_methods=["*"],
    allow_headers=["*"],
)
#users
app.include_router(auth_router, prefix="/auth/jwt", tags=["auth"])
app.include_router(register_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

#others
app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(plan_router, prefix="/plan", tags=["plans"])
app.include_router(skill_router, prefix="/skill", tags=["skill"])
app.include_router(salary_router, prefix="/salary", tags=["salary"])

#agent
app.include_router(agent_router, prefix="/chat", tags=["agent"])
@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI!"}