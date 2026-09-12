from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    parent_topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="not_started")  # not_started, in_progress, completed
    order = Column(Integer, default=0)
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)
    prerequisites = Column(JSON, default=list)  # list of prerequisite topic IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        if "status" not in kwargs:
            kwargs["status"] = "not_started"
        if "position_x" not in kwargs:
            kwargs["position_x"] = 0.0
        if "position_y" not in kwargs:
            kwargs["position_y"] = 0.0
        if "prerequisites" not in kwargs:
            kwargs["prerequisites"] = []
        if "order" not in kwargs:
            kwargs["order"] = 0
        super().__init__(**kwargs)

