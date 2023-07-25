from typing import Optional

from fastapi import APIRouter, Depends, status

from auth.config import current_user
from auth.schemas import UserRead
from post.permission import author_permission
from post.schemas import PostCreate, PostRead, PostUpdate
from post.services import post_service

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(new_post: PostCreate, user: UserRead = Depends(current_user)):
    created_post = await post_service.create(user.id, new_post)
    return created_post


@router.post("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int, update_post: PostUpdate, user: UserRead = Depends(author_permission)
):
    updated_post = await post_service.update(post_id, update_post)
    return updated_post


@router.get("/", response_model=list[PostRead], status_code=status.HTTP_200_OK)
async def post_list(limit: int = 5, offset: Optional[int] = None):
    post_list = await post_service.list(limit=limit, offset=offset)
    return post_list


@router.get("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def get_post(post_id: int):
    post = await post_service.get(post_id)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user: UserRead = Depends(author_permission)):
    post_id = await post_service.delete(post_id)
