import pytest
from httpx import AsyncClient

from src.post.repository import PostRepository
from src.post.schemas import PostRead


async def test_post_get_list(client: AsyncClient, user1_posts: list[PostRead]) -> None:
    response = await client.get("/post/")
    assert response.status_code == 200
    assert len(response.json()) == len(user1_posts)


async def test_post_get(client, user1_post: PostRead) -> None:
    response = await client.get(f"/post/{user1_post.id}")
    assert response.status_code == 200
    assert response.json()["id"] == user1_post.id


@pytest.mark.parametrize(
    "data, code, number",
    [
        ({"text": "string", "published": True}, 201, 1),
        ({}, 422, 0),
    ]
)
async def test_create_post(
    user1_client: AsyncClient, data: dict, code: int, number: int
) -> None:
    response = await user1_client.post("/post/", json=data)
    assert response.status_code == code
    async with PostRepository() as post_repo:
        posts = await post_repo.get_many()
    assert len(posts) == number


async def test_create_post_unauthorized(client):
    response = await client.post("/post/", json={"text": "string", "published": True})
    assert response.status_code == 401


async def test_update_post(user1_client: AsyncClient, user1_post):
    data = {"text": "updated_string", "published": True}
    response = await user1_client.post(f"/post/{user1_post.id}", json=data)
    assert response.status_code == 201
    assert response.json()["text"] == data["text"]


async def test_delete_own_post(user1_client: AsyncClient, user1_post):
    response = await user1_client.delete(f"/post/{user1_post.id}")
    assert response.status_code == 204
