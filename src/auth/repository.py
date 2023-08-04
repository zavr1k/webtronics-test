from sqlalchemy import select

from src.repository import BaseSQLAlchemyRepository

from .models import User


class UserRepository(BaseSQLAlchemyRepository):
    model = User

    async def get_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)
        user = await self.session.execute(query)
        return user.scalar_one()
