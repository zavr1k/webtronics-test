from typing import Optional

from config import FETCH_LIMIT
from post.repository import PostRepository
from src.post.schemas import PostCreate, PostRead, PostUpdate


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
        return post

    async def list(self, limit: int = 5, offset: Optional[int] = None):
        limit = min(max(limit, 0), FETCH_LIMIT)
        res = await self.post_repo.get_many(limit=limit, offset=offset)
        return res

    async def update(self, post_id: int, update_post: PostUpdate):
        post_dict = update_post.model_dump() 
        post_dict = {k: v for k, v in post_dict.items() if v is not None}
        updated_post = await self.post_repo.update(post_id, post_dict)
        return updated_post
    
    async def delete(self, post_id: int):
        res = await self.post_repo.delete(post_id)
        return res


post_service = PostService()
