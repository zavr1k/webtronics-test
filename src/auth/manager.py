from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from auth.models import User
from auth.utils import get_user_db
from src.config import USER_MANAGER_SECRET_RESET, USER_MANAGER_SECRET_VERIFY


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_MANAGER_SECRET_RESET
    verification_token_secret = USER_MANAGER_SECRET_VERIFY


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
