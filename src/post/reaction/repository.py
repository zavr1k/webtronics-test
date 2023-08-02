from typing import Optional

from sqlalchemy import delete, func, insert, select

from src.repository import BaseSQLAlchemyRepository

from .models import Reaction
from .schemas import ReactionRead
from .types import ReactionType


class ReactionRepository(BaseSQLAlchemyRepository):
    model = Reaction

    async def create(self, data: dict):
        stmt = (
            insert(self.model)
            .values(**data)
            .returning(
                self.model.user_id,
                self.model.post_id,
            )
        )
        insert_result = await self.session.execute(stmt)
        user_id, post_id = insert_result.one()
        return await self.get_one(post_id, user_id)

    async def get_one(self, post_id: int, user_id: int) -> ReactionRead:
        query = (
            select(self.model)
            .where(self.model.post_id == post_id, self.model.user_id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one().to_read_model()

    async def delete(self, post_id: int, user_id: int) -> int:
        stmt = (
            delete(self.model)
            .where(self.model.post_id == post_id, self.model.user_id == user_id)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        r = result.scalar_one()
        await self.session.commit()
        return r

    async def get_many(
        self,
        post_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[ReactionRead]:
        query = select(self.model).where(self.model.post_id == post_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return [post.to_read_model() for post in result.scalars().all()]

    async def count(self, post_id: int, reaction: Optional[ReactionType] = None) -> int:
        query = (
            select(func.count(self.model.id))
            .where(self.model.post_id == post_id)
        )
        if reaction:
            query = query.where(self.model.reaction == reaction)
        result = await self.session.execute(query)
        return result.scalar_one()
