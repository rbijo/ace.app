from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubjectBase(BaseModel):
    title: str
    code: Optional[str] = None
    description: Optional[str] = None


class SubjectCreate(SubjectBase):
    course_id: int


class SubjectResponse(SubjectBase):
    id: int
    course_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

