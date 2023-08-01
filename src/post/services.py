from typing import Optional

from src.config import settings
from src.post.reaction.services import reaction_service
from src.post.repository import PostRepository
from src.post.schemas import PostCreate, PostRead, PostUpdate


class PostService:
    def __init__(self, repo) -> None:
        self.repository = repo

    async def create(self, user_id: int, new_post: PostCreate):
        post_dict = new_post.model_dump()
        post_dict["author_id"] = user_id
        async with self.repository() as post_repo:
            created_post = await post_repo.create(post_dict)
        return created_post

    async def get(self, post_id: int) -> PostRead:
        async with self.repository() as post_repo:
            post = await post_repo.get_one(pk=post_id)
        post.likes = await reaction_service.count_likes(post.id)
        post.dislikes = await reaction_service.count_dislikes(post.id)
        return post

    async def list(self, limit: int = 5, offset: Optional[int] = None):
        limit = min(max(limit, 0), settings.FETCH_LIMIT)
        async with self.repository() as post_repo:
            post_list = await post_repo.get_many(limit=limit, offset=offset)
        for post in post_list:
            post.likes = await reaction_service.count_likes(post.id)
            post.dislikes = await reaction_service.count_dislikes(post.id)
        return post_list

    async def update(self, post_id: int, update_post: PostUpdate):
        post_dict = update_post.model_dump()
        post_dict = {k: v for k, v in post_dict.items() if v is not None}
        async with self.repository() as post_repo:
            updated_post = await post_repo.update(post_id, post_dict)
        updated_post.likes = await reaction_service.count_likes(updated_post.id)
        updated_post.dislikes = await reaction_service.count_dislikes(updated_post.id)
        return updated_post

    async def delete(self, post_id: int):
        async with self.repository() as post_repo:
            res = await post_repo.delete(post_id)
        return res


post_service = PostService(PostRepository)
