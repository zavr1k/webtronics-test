from .repository import UserRepository
from .schemas import UserDB


class UserService:
    def __init__(self, repo) -> None:
        self.repository = repo

    async def get_by_username(self, username: str) -> UserDB:
        async with self.repository() as user_repo:
            user = await user_repo.get_by_username(username)
            return user.to_db_model()


user_service = UserService(UserRepository)
