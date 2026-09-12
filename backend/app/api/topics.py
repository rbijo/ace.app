from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate, TopicResponse
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.post("", response_model=TopicResponse)
async def create_topic(
    topic_in: TopicCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = Topic(
        subject_id=topic_in.subject_id,
        parent_topic_id=topic_in.parent_topic_id,
        title=topic_in.title,
        description=topic_in.description,
        status=topic_in.status or "not_started",
        order=topic_in.order or 0,
        position_x=topic_in.position_x or 0.0,
        position_y=topic_in.position_y or 0.0,
        prerequisites=topic_in.prerequisites or []
    )
    db.add(topic)
    await db.commit()
    await db.refresh(topic)

    # Recalculate progress ratio
    await ProgressService.calculate_subject_progress(db, current_user.id, topic.subject_id)
    return topic


@router.get("/subject/{subject_id}", response_model=List[TopicResponse])
async def list_topics_for_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Topic).where(Topic.subject_id == subject_id).order_by(Topic.order)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.patch("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: int,
    topic_in: TopicUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Topic).where(Topic.id == topic_id)
    res = await db.execute(stmt)
    topic = res.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    update_data = topic_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(topic, field, value)

    await db.commit()
    await db.refresh(topic)

    # Recalculate percentage progress
    await ProgressService.calculate_subject_progress(db, current_user.id, topic.subject_id)
    return topic

