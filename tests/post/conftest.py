import pytest

from src.post.repository import PostRepository
from src.post.schemas import PostRead


@pytest.fixture
async def post1_user1(user1) -> PostRead:
    async with PostRepository() as post_repo:
        return await post_repo.create({
            "author_id": user1.id,
            "text": "string",
            "published": True,
        })


@pytest.fixture
async def post2_user1(user1) -> list[PostRead]:
    async with PostRepository() as post_repo:
        post1 = await post_repo.create({
            "author_id": user1.id,
            "text": "post1",
            "published": True,
        })
        post2 = await post_repo.create({
            "author_id": user1.id,
            "text": "post2",
            "published": True,
        })
        return [post1, post2]
