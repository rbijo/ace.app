from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# For SQLite, async engine requires sqlite+aiosqlite
db_url = settings.DATABASE_URL
if db_url.startswith("sqlite://"):
    db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")

# Supabase Transaction Pooler (PgBouncer) does not support
# asyncpg prepared statements correctly in transaction mode.
connect_args = {}
if db_url.startswith("postgresql+asyncpg://"):
    connect_args = {"statement_cache_size": 0}

engine = create_async_engine(
    db_url,
    echo=False,
    future=True,
    connect_args=connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session