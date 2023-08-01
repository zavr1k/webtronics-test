import pytest
from httpx import AsyncClient

from src.post.repository import PostRepository
from src.post.schemas import PostRead


async def test_post_get_list(client: AsyncClient, post2_user1: list[PostRead]) -> None:
    response = await client.get("/post/")
    assert response.status_code == 200
    assert len(response.json()) == len(post2_user1)


async def test_post_get(client, post1_user1: PostRead) -> None:
    response = await client.get(f"/post/{post1_user1.id}")
    assert response.status_code == 200
    assert response.json()["id"] == post1_user1.id


@pytest.mark.parametrize(
    "data, code, number",
    [
        ({"text": "string", "published": True}, 201, 1),
        ({}, 422, 0),
    ]
)
async def test_create_post(
    logged_client1: AsyncClient, data: dict, code: int, number: int
) -> None:
    response = await logged_client1.post("/post/", json=data)
    assert response.status_code == code
    async with PostRepository() as post_repo:
        posts = await post_repo.get_many()
    assert len(posts) == number


async def test_create_post_unauthorized(client):
    response = await client.post("/post/", json={"text": "string", "published": True})
    assert response.status_code == 401


async def test_update_post(logged_client1: AsyncClient, post1_user1):
    data = {"text": "updated_string", "published": True}
    response = await logged_client1.post(f"/post/{post1_user1.id}", json=data)
    assert response.status_code == 201
    assert response.json()["text"] == data["text"]


async def test_delete_own_post(logged_client1: AsyncClient, post1_user1):
    response = await logged_client1.delete(f"/post/{post1_user1.id}")
    assert response.status_code == 204
