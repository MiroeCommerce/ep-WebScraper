# # File: app/core/database.py
"""Database connection and session management for the application."""

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from data_ingestion_service.app.core.config import settings


class Database: # May need to remove the url from here, and pass it and create the db in the main.py
    def __init__(self):
        self.engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def session_scope(self):
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

class Base(DeclarativeBase):
    pass