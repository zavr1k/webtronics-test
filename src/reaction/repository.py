from typing import Optional

from sqlalchemy import delete, select

from database import async_session_maker
from repository import BaseSQLAlchemyRepository

from .models import Reaction
from .schemas import ReactionRead


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
