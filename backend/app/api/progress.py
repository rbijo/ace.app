from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.progress import ProgressResponse
from app.services.progress_service import ProgressService
from app.services.motivation_service import MotivationService

router = APIRouter(prefix="/progress", tags=["Progress Engine"])


class ProgressWithMotivation(ProgressResponse):
    motivation_message: str


@router.get("/subject/{subject_id}", response_model=ProgressWithMotivation)
async def get_subject_progress(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = await ProgressService.calculate_subject_progress(db, current_user.id, subject_id)
    message = MotivationService.get_encouragement_message(
        percentage=progress.percentage_complete,
        completed_count=progress.completed_topics
    )
    return ProgressWithMotivation(
        subject_id=progress.subject_id,
        total_topics=progress.total_topics,
        completed_topics=progress.completed_topics,
        percentage_complete=progress.percentage_complete,
        last_updated=progress.last_updated,
        motivation_message=message
    )

