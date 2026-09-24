from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import get_config

@lru_cache
def get_engine():
    return create_async_engine(
        get_config().db.get_async_db_url(),
        echo=True,
        pool_size=20,
        max_overflow=40,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

@lru_cache
def get_session_factory():
    return async_sessionmaker(bind=get_engine(), expire_on_commit=False, class_=AsyncSession,)

async def get_db():
    AsyncSessionLocal = get_session_factory()
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

DBSession = Annotated[AsyncSession, Depends(get_db)]
