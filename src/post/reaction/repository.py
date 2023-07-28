from typing import Optional

from sqlalchemy import delete, func, select

from database import async_session_maker
from src.repository import BaseSQLAlchemyRepository

from .models import Reaction
from .schemas import ReactionRead
from .types import ReactionType


class ReactionRepository(BaseSQLAlchemyRepository):
    model = Reaction

    async def get(self, post_id: int, user_id: int) -> ReactionRead:
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .where(self.model.post_id == post_id, self.model.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalar_one().to_read_model()

    async def delete(self, post_id: int, user_id: int) -> int:
        async with async_session_maker() as session:
            stmt = (
                delete(self.model)
                .where(self.model.post_id == post_id, self.model.user_id == user_id)
                .returning(self.model.id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def get_many(
        self,
        post_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[ReactionRead]:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.post_id == post_id)
            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            result = await session.execute(query)
            return [post.to_read_model() for post in result.scalars().all()]

    async def count(self, post_id: int, reaction: Optional[ReactionType] = None) -> int:
        async with async_session_maker() as session:
            query = (
                select(func.count(self.model.id))
                .where(self.model.post_id == post_id)
            )
            if reaction:
                query = query.where(self.model.reaction == reaction)
            result = await session.execute(query)
            return result.scalar_one()
