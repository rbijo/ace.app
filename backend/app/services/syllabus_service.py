import re
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.topic import Topic


class SyllabusService:

    @staticmethod
    async def parse_and_create_topics(db: AsyncSession, subject_id: int, text: str) -> List[Topic]:
        """Extract lines or headings from syllabus text and save as topic nodes"""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        created_topics = []

        for index, line in enumerate(lines):
            # Clean section numbering like "1. Introduction" or "Module 2: Arrays"
            clean_title = re.sub(r'^(Module\s+\d+:?|\d+[\.\)]\s*)', '', line, flags=re.IGNORECASE).strip()
            if not clean_title:
                clean_title = line

            topic = Topic(
                subject_id=subject_id,
                title=clean_title[:100],
                description=f"Automated topic node generated from syllabus line {index + 1}",
                order=index + 1,
                position_x=float((index % 3) * 250),
                position_y=float((index // 3) * 120),
                parent_topic_id=created_topics[-1].id if created_topics and index % 3 != 0 else None,
                status="not_started"
            )
            db.add(topic)
            await db.flush()
            created_topics.append(topic)

        await db.commit()
        for t in created_topics:
            await db.refresh(t)
        return created_topics

