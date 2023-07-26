from typing import Optional

from sqlalchemy.exc import NoResultFound

from config import FETCH_LIMIT
from post.repository import PostRepository, ReactionRepository
from src.post.schemas import (PostCreate, PostRead, PostUpdate, ReactionCreate,
                              ReactionRead)

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


class PostService:
    def __init__(self) -> None:
        self.post_repo = PostRepository()

    async def create(self, user_id: int, new_post: PostCreate):
        post_dict = new_post.model_dump() 
        post_dict["author_id"] = user_id
        created_post = await self.post_repo.create(post_dict)
        return created_post

    async def get(self, post_id: int) -> PostRead:
        post = await self.post_repo.get_one(pk=post_id)
        post.likes = await reaction_service.count_likes(post.id)
        post.dislikes = await reaction_service.count_dislikes(post.id)
        return post

    async def list(self, limit: int = 5, offset: Optional[int] = None):
        limit = min(max(limit, 0), FETCH_LIMIT)
        post_list = await self.post_repo.get_many(limit=limit, offset=offset)
        for post in post_list:
            post.likes = await reaction_service.count_likes(post.id)
            post.dislikes = await reaction_service.count_dislikes(post.id)
        return post_list

    async def update(self, post_id: int, update_post: PostUpdate):
        post_dict = update_post.model_dump() 
        post_dict = {k: v for k, v in post_dict.items() if v is not None}
        updated_post = await self.post_repo.update(post_id, post_dict)
        updated_post.likes = await reaction_service.count_likes(updated_post.id)
        updated_post.dislikes = await reaction_service.count_dislikes(updated_post.id)
        return updated_post
    
    async def delete(self, post_id: int):
        res = await self.post_repo.delete(post_id)
        return res


post_service = PostService()
