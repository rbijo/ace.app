from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.learning import RoadmapResponse
from app.services.learning_service import LearningService

router = APIRouter(prefix="/learning", tags=["Learning Engine"])


@router.get("/roadmap/{subject_id}", response_model=RoadmapResponse)
async def get_roadmap_flowchart(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roadmap = await LearningService.get_roadmap_flowchart(db, current_user.id, subject_id)
    return roadmap

