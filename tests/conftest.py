import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.auth.config import create_user, current_user
from src.auth.schemas import UserRead
from src.config import settings
from src.database import Base, get_async_session
from src.main import app

engine_test = create_async_engine(f"{settings.DATABASE_URL}")
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
def check_test_database():
    if 'test' not in settings.POSTGRES_DB:
        raise ValueError(
            f'Test database name must include word "test"'
            f'current database {settings.POSTGRES_DB}'
        )


@pytest.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture()
async def user1() -> UserRead:
    user = await create_user("test_user1@example.com", "user1", "password")
    return user


@pytest.fixture()
async def user2() -> UserRead:
    user = await create_user("test_user2@example.com", "user2", "password")
    return user


@pytest.fixture()
async def user1_client(user1: UserRead) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[current_user] = lambda: user1
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
    app.dependency_overrides[current_user] = current_user


@pytest.fixture()
async def user2_client(user2: UserRead) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[current_user] = lambda: user2
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
    app.dependency_overrides[current_user] = current_user
