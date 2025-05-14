from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)
async_session_factory = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


# Генератор сессий
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_factory() as session:
#         yield session
