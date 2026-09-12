from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    parent_topic_id: Optional[int] = None
    status: Optional[str] = "not_started"
    order: Optional[int] = 0
    position_x: Optional[float] = 0.0
    position_y: Optional[float] = 0.0
    prerequisites: Optional[List[int]] = []


class TopicCreate(TopicBase):
    subject_id: int


class TopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    parent_topic_id: Optional[int] = None
    status: Optional[str] = None
    order: Optional[int] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    prerequisites: Optional[List[int]] = None


class TopicResponse(TopicBase):
    id: int
    subject_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

