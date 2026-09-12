from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.topic import TopicResponse
from app.services.syllabus_service import SyllabusService

router = APIRouter(prefix="/syllabus", tags=["Syllabus Engine"])


class SyllabusParseRequest(BaseModel):
    subject_id: int
    content: str


@router.post("/parse", response_model=List[TopicResponse])
async def parse_syllabus_text(
    payload: SyllabusParseRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topics = await SyllabusService.parse_and_create_topics(
        db=db,
        subject_id=payload.subject_id,
        text=payload.content
    )
    return topics

