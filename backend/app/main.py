from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, courses, subjects, topics, learning, tasks, progress, ai, syllabus


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(courses.router, prefix=settings.API_V1_STR)
app.include_router(subjects.router, prefix=settings.API_V1_STR)
app.include_router(topics.router, prefix=settings.API_V1_STR)
app.include_router(learning.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)
app.include_router(progress.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(syllabus.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to ACE Backend API", "docs": "/docs"}


@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "ok", "version": settings.VERSION}

