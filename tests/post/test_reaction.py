from httpx import AsyncClient

from src.post.reaction.repository import ReactionRepository
from src.post.reaction.schemas import ReactionRead
from src.post.reaction.types import ReactionType
from src.post.schemas import PostRead


async def test_reaction_get_list(client: AsyncClient, user1_post: PostRead) -> None:
    response = await client.get(f"/post/{user1_post.id}/reaction/")
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_reaction_set_like(
    user2_client: AsyncClient, user1_post: PostRead
) -> None:
    data = {"reaction": ReactionType.LIKE.value, "post_id": user1_post.id}
    response = await user2_client.post(f"/post/{user1_post.id}/reaction/", json=data)
    async with ReactionRepository() as repo:
        reactions = await repo.get_many(user1_post.id)
    assert response.status_code == 201
    assert len(reactions) == 1
    assert reactions[0].reaction == ReactionType.LIKE


async def test_reaction_set_own_post_like(
    user1_client: AsyncClient, user1_post: PostRead
) -> None:
    data = {"reaction": ReactionType.LIKE, "post_id": user1_post.id}
    response = await user1_client.post(f"/post/{user1_post.id}/reaction/", json=data)
    assert response.status_code == 403


async def test_reaction_delete(
    user2_client: AsyncClient, post1_like: ReactionRead
) -> None:
    response = await user2_client.delete(f"/post/{post1_like.post_id}/reaction/")
    assert response.status_code == 204
    async with ReactionRepository() as reaction_repo:
        reactions = await reaction_repo.get_many(post1_like.post_id)
    assert len(reactions) == 0
