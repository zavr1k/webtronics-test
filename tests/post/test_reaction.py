from httpx import AsyncClient

from src.post.reaction.repository import ReactionRepository
from src.post.reaction.schemas import ReactionRead
from src.post.reaction.types import ReactionType
from src.post.schemas import PostRead


async def test_reaction_get_list(client: AsyncClient, post1_user1: PostRead) -> None:
    response = await client.get(f"/post/{post1_user1.id}/reaction/")
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_reaction_set_like(
    logged_client2: AsyncClient, post1_user1: PostRead
) -> None:
    data = {"reaction": ReactionType.LIKE.value, "post_id": post1_user1.id}
    response = await logged_client2.post(f"/post/{post1_user1.id}/reaction/", json=data)
    async with ReactionRepository() as repo:
        reactions = await repo.get_many(post1_user1.id)
    assert response.status_code == 201
    assert len(reactions) == 1
    assert reactions[0].reaction == ReactionType.LIKE


async def test_reaction_set_own_post_like(
    logged_client1: AsyncClient, post1_user1: PostRead
) -> None:
    data = {"reaction": ReactionType.LIKE, "post_id": post1_user1.id}
    response = await logged_client1.post(f"/post/{post1_user1.id}/reaction/", json=data)
    assert response.status_code == 403


async def test_reaction_delete(
    logged_client2: AsyncClient, liked_post1: ReactionRead
) -> None:
    response = await logged_client2.delete(f"/post/{liked_post1.post_id}/reaction/")
    assert response.status_code == 204
    async with ReactionRepository() as reaction_repo:
        reactions = await reaction_repo.get_many(liked_post1.post_id)
    assert len(reactions) == 0
