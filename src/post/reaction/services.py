from typing import Optional

from sqlalchemy.exc import NoResultFound

from config import FETCH_LIMIT

from .repository import ReactionRepository
from .schemas import ReactionCreate, ReactionRead
from .types import ReactionType


class ReactionService:
    def __init__(self) -> None:
        self.reaction_repo = ReactionRepository()

    async def set(
        self,
        user_id: int,
        post_id: int,
        new_reaction: ReactionCreate,
    ) -> ReactionRead:
        reaction_dict = new_reaction.model_dump() 
        reaction_dict["post_id"] = post_id
        reaction_dict["user_id"] = user_id
        try:
            db_reaction = await self.reaction_repo.get(post_id, user_id)
        except NoResultFound:
            reaction = await self.reaction_repo.create(reaction_dict)
        else:
            reaction = await self.reaction_repo.update(db_reaction.id, reaction_dict)
        return reaction

    async def list(
        self,
        post_id: int,
        limit: int = 5,
        offset: Optional[int] = None
    ) -> list[ReactionRead]:
        limit = min(max(limit, 0), FETCH_LIMIT)
        reactions = await self.reaction_repo.get_many(post_id=post_id, limit=limit, offset=offset)
        return reactions

    async def delete(self, post_id: int, user_id: int) -> int:
        res = await self.reaction_repo.delete(post_id, user_id)
        return res

    async def count_likes(self, post_id: int) -> int:
        return await self.reaction_repo.count(post_id, ReactionType.LIKE)

    async def count_dislikes(self, post_id: int) -> int:
        return await self.reaction_repo.count(post_id, ReactionType.DISLIKE)


reaction_service = ReactionService()
