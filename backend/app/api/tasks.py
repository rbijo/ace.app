from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.task import Task
from app.models.topic import Topic
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/tasks", tags=["Tasks Engine"])


class TaskCreate(BaseModel):
    topic_id: int
    title: str
    description: Optional[str] = None
    task_type: Optional[str] = "reading"
    estimated_minutes: Optional[int] = 30


class TaskResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    description: Optional[str] = None
    task_type: str
    estimated_minutes: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)


@router.post("", response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = Task(
        topic_id=task_in.topic_id,
        title=task_in.title,
        description=task_in.description,
        task_type=task_in.task_type or "reading",
        estimated_minutes=task_in.estimated_minutes or 30
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Task).where(Task.id == task_id)
    res = await db.execute(stmt)
    task = res.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    await db.commit()
    await db.refresh(task)

    # Also update topic status if all tasks completed
    topic_stmt = select(Topic).where(Topic.id == task.topic_id)
    topic_res = await db.execute(topic_stmt)
    topic = topic_res.scalar_one_or_none()
    if topic:
        tasks_stmt = select(Task).where(Task.topic_id == topic.id)
        tasks_res = await db.execute(tasks_stmt)
        all_tasks = tasks_res.scalars().all()
        if all_tasks and all(t.completed for t in all_tasks):
            topic.status = "completed"
            await db.commit()
            await ProgressService.calculate_subject_progress(db, current_user.id, topic.subject_id)

    return task

