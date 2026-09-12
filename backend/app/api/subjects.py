from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.subject import Subject
from app.schemas.course import SubjectCreate, SubjectResponse

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("", response_model=SubjectResponse)
async def create_subject(
    subject_in: SubjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subject = Subject(
        course_id=subject_in.course_id,
        title=subject_in.title,
        code=subject_in.code,
        description=subject_in.description
    )
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    return subject


@router.get("/course/{course_id}", response_model=List[SubjectResponse])
async def list_subjects_for_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Subject).where(Subject.course_id == course_id)
    res = await db.execute(stmt)
    return res.scalars().all()

