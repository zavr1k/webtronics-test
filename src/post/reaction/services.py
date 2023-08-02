from typing import Optional

from sqlalchemy.exc import NoResultFound

from src.cache import cache
from src.config import settings

from .repository import ReactionRepository
from .schemas import ReactionCreate, ReactionRead
from .types import ReactionType


class ReactionService:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def set(
        self,
        user_id: int,
        post_id: int,
        new_reaction: ReactionCreate,
    ) -> ReactionRead:
        reaction_dict = new_reaction.model_dump()
        reaction_dict["post_id"] = post_id
        reaction_dict["user_id"] = user_id
        async with self.repository() as reaction_repo:
            try:
                db_reaction = await reaction_repo.get_one(post_id, user_id)
            except NoResultFound:
                reaction = await reaction_repo.create(reaction_dict)
            else:
                reaction = await reaction_repo.update(db_reaction.id, reaction_dict)

        await self.count_likes(post_id, force=True)
        await self.count_dislikes(post_id, force=True)
        return reaction

    async def list(
        self,
        post_id: int,
        limit: int = 5,
        offset: Optional[int] = None
    ) -> list[ReactionRead]:
        limit = min(max(limit, 0), settings.FETCH_LIMIT)
        async with self.repository() as reaction_repo:
            reactions = await reaction_repo.get_many(
                post_id=post_id,
                limit=limit,
                offset=offset
            )
        return reactions

    async def delete(self, post_id: int, user_id: int) -> int:
        async with self.repository() as reaction_repo:
            res = await reaction_repo.delete(post_id, user_id)

        await self.count_likes(res, force=True)
        await self.count_dislikes(res, force=True)
        return res

    async def count_likes(self, post_id: int, force: bool = False) -> int:
        cached_name = f"post:{post_id}:{ReactionType.LIKE.value}"
        likes = await cache.get_key(cached_name)
        if not likes or force:
            async with self.repository() as reaction_repo:
                likes = await reaction_repo.count(post_id, ReactionType.LIKE)
            await cache.set_key(cached_name, likes)
        return int(likes)

    async def count_dislikes(self, post_id: int, force: bool = False) -> int:
        cached_name = f"post:{post_id}:{ReactionType.DISLIKE.value}"
        dislikes = await cache.get_key(cached_name)
        if not dislikes or force:
            async with self.repository() as reaction_repo:
                dislikes = await reaction_repo.count(post_id, ReactionType.DISLIKE)
            await cache.set_key(cached_name, dislikes)
        return int(dislikes)


reaction_service = ReactionService(ReactionRepository)
