from typing import AsyncGenerator

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from config import DATABASE_URL

Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Model(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
