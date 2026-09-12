from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from app.models.topic import Topic
from app.models.subject import Subject
from app.schemas.learning import FlowNode, FlowEdge, RoadmapResponse
from app.schemas.topic import TopicResponse
from app.services.progress_service import ProgressService


class LearningService:

    @staticmethod
    async def get_roadmap_flowchart(db: AsyncSession, user_id: int, subject_id: int) -> RoadmapResponse:
        # Fetch subject details
        subj_stmt = select(Subject).where(Subject.id == subject_id)
        subj_res = await db.execute(subj_stmt)
        subject = subj_res.scalar_one_or_none()
        subject_title = subject.title if subject else f"Subject #{subject_id}"

        # Fetch all topics for subject
        topics_stmt = select(Topic).where(Topic.subject_id == subject_id).order_by(Topic.order)
        topics_res = await db.execute(topics_stmt)
        topics = list(topics_res.scalars().all())

        nodes: List[FlowNode] = []
        edges: List[FlowEdge] = []
        next_recommended: List[TopicResponse] = []

        completed_ids = set(t.id for t in topics if t.status == "completed")

        for index, topic in enumerate(topics):
            # Calculate position layout for flowchart UI
            pos_x = topic.position_x if topic.position_x != 0.0 else float((index % 3) * 250)
            pos_y = topic.position_y if topic.position_y != 0.0 else float((index // 3) * 120)

            node = FlowNode(
                id=str(topic.id),
                label=topic.title,
                status=topic.status or "not_started",
                position_x=pos_x,
                position_y=pos_y
            )
            nodes.append(node)

            # Build edges from parent_topic_id
            if topic.parent_topic_id:
                edges.append(FlowEdge(
                    id=f"e-{topic.parent_topic_id}-{topic.id}",
                    source=str(topic.parent_topic_id),
                    target=str(topic.id)
                ))

            # Build edges from prerequisites list
            if topic.prerequisites and isinstance(topic.prerequisites, list):
                for prereq_id in topic.prerequisites:
                    edges.append(FlowEdge(
                        id=f"e-{prereq_id}-{topic.id}",
                        source=str(prereq_id),
                        target=str(topic.id)
                    ))

            # Determine next recommended topics (uncompleted topics whose prerequisites are met)
            if topic.status != "completed":
                prereqs = topic.prerequisites or []
                if not prereqs or all(int(p) in completed_ids for p in prereqs):
                    next_recommended.append(TopicResponse.model_validate(topic))

        # Calculate progress
        progress_rec = await ProgressService.calculate_subject_progress(db, user_id, subject_id)
        pct = progress_rec.percentage_complete if progress_rec else 0.0

        return RoadmapResponse(
            subject_id=subject_id,
            subject_title=subject_title,
            percentage_complete=pct,
            nodes=nodes,
            edges=edges,
            next_recommended_topics=next_recommended
        )

