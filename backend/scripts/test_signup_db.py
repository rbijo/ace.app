import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from sqlalchemy import select


async def test_signup_connection():
    print("Testing signup database connection...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        test_email = "newstudent@ace.app"
        test_pass = "StudentPass2026!"

        # Check existing
        stmt = select(User).where(User.email == test_email)
        res = await db.execute(stmt)
        user = res.scalar_one_or_none()

        if not user:
            user = User(
                email=test_email,
                full_name="New ACE Student",
                hashed_password=get_password_hash(test_pass)
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print(f"SUCCESS: Created new student user ID #{user.id} in DB.")
        else:
            print(f"SUCCESS: Found existing student user ID #{user.id} in DB.")

        assert verify_password(test_pass, user.hashed_password) is True
        print(f"SUCCESS: Password verification passed for {user.email}.")


if __name__ == "__main__":
    asyncio.run(test_signup_connection())

