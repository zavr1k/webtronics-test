import contextlib

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from src.config import settings
from src.database import get_async_session

from .manager import get_user_manager
from .models import User
from .schemas import UserCreate, UserRead
from .utils import get_user_db

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str, username: str, password: str, is_superuser: bool = False
) -> UserRead:
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.create(
                    UserCreate(
                        email=email,
                        username=username,
                        password=password,
                        is_superuser=is_superuser,
                    )
                )
    return user.to_read_model()
