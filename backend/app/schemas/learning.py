from pydantic import BaseModel
from typing import List, Optional
from app.schemas.topic import TopicResponse


class FlowNode(BaseModel):
    id: str
    label: str
    status: str
    position_x: float
    position_y: float


class FlowEdge(BaseModel):
    id: str
    source: str
    target: str


class RoadmapResponse(BaseModel):
    subject_id: int
    subject_title: str
    percentage_complete: float
    nodes: List[FlowNode]
    edges: List[FlowEdge]
    next_recommended_topics: List[TopicResponse]

