from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.config import settings

from .models import User
from .utils import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.USER_MANAGER_SECRET_RESET
    verification_token_secret = settings.USER_MANAGER_SECRET_VERIFY


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
