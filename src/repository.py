from typing import Optional

from sqlalchemy import delete, insert, select, update

from src.database import Model, async_session_maker


class BaseSQLAlchemyRepository:
    model = Model

    async def __aenter__(self):
        self.session = async_session_maker()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_type or exc_value or exc_traceback:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    async def create(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)
        insert_result = await self.session.execute(stmt)
        return await self.get_one(insert_result.scalar_one())

    async def get_one(self, pk: int):
        query = select(self.model).where(self.model.id == pk)
        result = await self.session.execute(query)
        return result.scalar_one().to_read_model()

    async def get_many(self, limit: Optional[int] = None, offset: Optional[int] = None):
        query = select(self.model)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return [post.to_read_model() for post in result.scalars().all()]

    async def update(self, pk: int, data: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == pk)
            .values(**data)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return await self.get_one(result.scalar_one())

    async def delete(self, pk: int):
        stmt = (
            delete(self.model)
            .where(self.model.id == pk)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
