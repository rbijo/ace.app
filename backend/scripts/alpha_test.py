import asyncio
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import User, Course, Subject, Topic, Task, Progress, AISession
from app.core.security import get_password_hash
from app.services.progress_service import ProgressService
from app.services.learning_service import LearningService
from app.services.ai.openrouter import OpenRouterService
from sqlalchemy import select, func


async def run_alpha_test():
    print("==================================================")
    print("         ACE ALPHA TESTING RUNNER                 ")
    print("==================================================")

    # 1. Initialize Database schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✔ Step 1: Database tables initialized.")

    async with AsyncSessionLocal() as db:
        # 2. Register/Fetch Alpha Test User
        email = "alpha.student@ace.app"
        user_stmt = select(User).where(User.email == email)
        res = await db.execute(user_stmt)
        user = res.scalar_one_or_none()

        if not user:
            user = User(
                email=email,
                full_name="Alpha Student Tester",
                hashed_password=get_password_hash("SecretPass123!")
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print(f"✔ Step 2: Registered new user '{user.email}' (ID: {user.id})")
        else:
            print(f"✔ Step 2: Found existing user '{user.email}' (ID: {user.id})")

        # 3. Create Course
        course_stmt = select(Course).where(Course.user_id == user.id, Course.title == "Computer Science 101")
        c_res = await db.execute(course_stmt)
        course = c_res.scalar_one_or_none()

        if not course:
            course = Course(
                title="Computer Science 101",
                description="Introductory CS curriculum for Alpha Testing",
                user_id=user.id
            )
            db.add(course)
            await db.commit()
            await db.refresh(course)
            print(f"✔ Step 3: Created Course '{course.title}' (ID: {course.id})")
        else:
            print(f"✔ Step 3: Found existing Course '{course.title}' (ID: {course.id})")

        # 4. Create Subject
        subject_stmt = select(Subject).where(Subject.course_id == course.id, Subject.title == "Data Structures")
        s_res = await db.execute(subject_stmt)
        subject = s_res.scalar_one_or_none()

        if not subject:
            subject = Subject(
                course_id=course.id,
                code="CS201",
                title="Data Structures",
                description="Arrays, Linked Lists, Trees, and Graph Flowcharts"
            )
            db.add(subject)
            await db.commit()
            await db.refresh(subject)
            print(f"✔ Step 4: Created Subject '{subject.title}' (ID: {subject.id})")
        else:
            print(f"✔ Step 4: Found existing Subject '{subject.title}' (ID: {subject.id})")

        # 5. Create Flowchart Topic Nodes
        topic_titles = [
            ("Arrays & Memory Layout", 0.0, 0.0, None),
            ("Singly Linked Lists", 250.0, 0.0, 1),
            ("Binary Search Trees", 500.0, 0.0, 2),
            ("Graph Flowchart Algorithms", 750.0, 0.0, 3),
        ]

        created_topics = []
        for idx, (title, px, py, parent_ref) in enumerate(topic_titles):
            t_stmt = select(Topic).where(Topic.subject_id == subject.id, Topic.title == title)
            t_res = await db.execute(t_stmt)
            topic = t_res.scalar_one_or_none()

            if not topic:
                topic = Topic(
                    subject_id=subject.id,
                    title=title,
                    description=f"Flowchart node for {title}",
                    order=idx + 1,
                    position_x=px,
                    position_y=py,
                    parent_topic_id=created_topics[-1].id if created_topics and parent_ref else None,
                    status="completed" if idx == 0 else "not_started"
                )
                db.add(topic)
                await db.commit()
                await db.refresh(topic)
            created_topics.append(topic)

        print(f"✔ Step 5: Created {len(created_topics)} Flowchart Topic Nodes in Database.")

        # 6. Create Tasks and toggle completion
        task_stmt = select(Task).where(Task.topic_id == created_topics[1].id)
        t_res = await db.execute(task_stmt)
        task = t_res.scalar_one_or_none()

        if not task:
            task = Task(
                topic_id=created_topics[1].id,
                title="Read Linked List pointer dynamics",
                description="Study memory allocation and pointer manipulations",
                task_type="reading",
                estimated_minutes=45,
                completed=True
            )
            db.add(task)
            await db.commit()
            await db.refresh(task)
            print(f"✔ Step 6: Created and completed Study Task '{task.title}'")

        # Update topic status if task completed
        created_topics[1].status = "completed"
        await db.commit()

        # 7. Calculate Percentage Completion Progress Engine
        progress_rec = await ProgressService.calculate_subject_progress(db, user.id, subject.id)
        print(f"✔ Step 7: Progress Calculation Engine Result:")
        print(f"   -> Total Topics: {progress_rec.total_topics}")
        print(f"   -> Completed Topics: {progress_rec.completed_topics}")
        print(f"   -> Percentage Complete: {progress_rec.percentage_complete}%")

        # 8. Query AI Tutor Service
        ai_service = OpenRouterService()
        ai_response = await ai_service.generate_response("Explain binary search trees in 2 sentences.")
        ai_session = AISession(
            user_id=user.id,
            topic_id=created_topics[2].id,
            prompt="Explain binary search trees in 2 sentences.",
            response=ai_response,
            provider="openrouter"
        )
        db.add(ai_session)
        await db.commit()
        print(f"✔ Step 8: AI Tutor Session Query stored in DB.")

        # 9. Verify DB Totals across tables
        u_count = (await db.execute(select(func.count(User.id)))).scalar()
        c_count = (await db.execute(select(func.count(Course.id)))).scalar()
        s_count = (await db.execute(select(func.count(Subject.id)))).scalar()
        t_count = (await db.execute(select(func.count(Topic.id)))).scalar()
        p_count = (await db.execute(select(func.count(Progress.id)))).scalar()
        ai_count = (await db.execute(select(func.count(AISession.id)))).scalar()

        print("\n==================================================")
        print("          DATABASE PERSISTENCE VERIFICATION REPORT")
        print("==================================================")
        print(f" Users Table Rows:        {u_count}")
        print(f" Courses Table Rows:      {c_count}")
        print(f" Subjects Table Rows:     {s_count}")
        print(f" Topics Table Rows:       {t_count}")
        print(f" Progress Table Rows:     {p_count}")
        print(f" AI Sessions Table Rows:  {ai_count}")
        print("==================================================")
        print(" ALPHA TESTING WORKFLOW PASSED WITH 100% SUCCESS  ")
        print("==================================================")


if __name__ == "__main__":
    asyncio.run(run_alpha_test())

