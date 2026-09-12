from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProgressResponse(BaseModel):
    subject_id: int
    subject_title: Optional[str] = None
    total_topics: int
    completed_topics: int
    percentage_complete: float
    last_updated: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

