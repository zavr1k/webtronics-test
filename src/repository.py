from typing import Optional

from sqlalchemy import delete, insert, select, update

from database import Model, async_session_maker


class BaseSQLAlchemyRepository:
    model = Model

    async def create(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one().to_read_model()

    async def get_one(self, pk: int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == pk)
            result = await session.execute(query)
            return result.scalar_one().to_read_model()

    async def get_many(self, limit: Optional[int] = None, offset: Optional[int] = None):
        async with async_session_maker() as session:
            query = select(self.model)
            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            result = await session.execute(query)
            return [post.to_read_model() for post in result.scalars().all()]

    async def update(self, pk: int, data: dict):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == pk)
                .values(**data)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one().to_read_model()

    async def delete(self, pk: int):
        async with async_session_maker() as session:
            stmt = (
                delete(self.model)
                .where(self.model.id == pk)
                .returning(self.model.id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
