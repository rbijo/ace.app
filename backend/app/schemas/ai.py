from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AIQueryRequest(BaseModel):
    prompt: str
    topic_id: Optional[int] = None
    provider: Optional[str] = "openrouter"


class AIQueryResponse(BaseModel):
    response: str
    provider: str
    topic_id: Optional[int] = None


class TopicExtractionRequest(BaseModel):
    subject_id: int
    syllabus_text: str


class ExtractedTopicItem(BaseModel):
    title: str
    description: Optional[str] = ""
    order: int
    prerequisites: Optional[List[str]] = []

