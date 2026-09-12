from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("", response_model=CourseResponse)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = Course(
        title=course_in.title,
        description=course_in.description,
        user_id=current_user.id
    )
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


@router.get("", response_model=List[CourseResponse])
async def list_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Course).where(Course.user_id == current_user.id)
    res = await db.execute(stmt)
    return res.scalars().all()

