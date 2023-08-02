import pytest

from src.post.reaction.repository import ReactionRepository
from src.post.reaction.schemas import ReactionRead
from src.post.reaction.types import ReactionType
from src.post.repository import PostRepository
from src.post.schemas import PostRead


@pytest.fixture
async def user1_post(user1) -> PostRead:
    async with PostRepository() as post_repo:
        return await post_repo.create({
            "author_id": user1.id,
            "text": "string",
            "published": True,
        })


@pytest.fixture
async def user1_posts(user1) -> list[PostRead]:
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


@pytest.fixture
async def post1_like(user1_post, user2) -> ReactionRead:
    async with ReactionRepository() as reaction_repo:
        res = await reaction_repo.create({
            "user_id": user2.id,
            "post_id": user1_post.id,
            "reaction": ReactionType.LIKE.value,
        })
        return res
