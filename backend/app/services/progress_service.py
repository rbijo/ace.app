from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.topic import Topic
from app.models.progress import Progress
from app.models.subject import Subject


class ProgressService:

    @staticmethod
    async def calculate_subject_progress(db: AsyncSession, user_id: int, subject_id: int) -> Progress:
        # Fetch total topics and completed topics count
        total_stmt = select(func.count(Topic.id)).where(Topic.subject_id == subject_id)
        total_res = await db.execute(total_stmt)
        total_topics = total_res.scalar() or 0

        completed_stmt = select(func.count(Topic.id)).where(
            Topic.subject_id == subject_id,
            Topic.status == "completed"
        )
        completed_res = await db.execute(completed_stmt)
        completed_topics = completed_res.scalar() or 0

        percentage = (completed_topics / total_topics * 100.0) if total_topics > 0 else 0.0

        # Check existing progress record
        stmt = select(Progress).where(Progress.user_id == user_id, Progress.subject_id == subject_id)
        res = await db.execute(stmt)
        progress_rec = res.scalar_one_or_none()

        if not progress_rec:
            progress_rec = Progress(
                user_id=user_id,
                subject_id=subject_id,
                total_topics=total_topics,
                completed_topics=completed_topics,
                percentage_complete=round(percentage, 2)
            )
            db.add(progress_rec)
        else:
            progress_rec.total_topics = total_topics
            progress_rec.completed_topics = completed_topics
            progress_rec.percentage_complete = round(percentage, 2)

        await db.commit()
        await db.refresh(progress_rec)
        return progress_rec

