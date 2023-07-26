from fastapi import APIRouter, Depends, status

from auth.schemas import UserRead

from .permission import like_permission
from .schemas import ReactionCreate, ReactionRead
from .services import reaction_service

router = APIRouter(prefix="/{post_id}/reaction")

@router.get("/", response_model=list[ReactionRead], status_code=status.HTTP_200_OK)
async def reaction_list(post_id: int):
    created_post = await reaction_service.list(post_id=post_id)
    return created_post


@router.post("/", response_model=ReactionRead, status_code=status.HTTP_201_CREATED)
async def set_reaction(
    post_id: int,
    new_reaction: ReactionCreate,
    user: UserRead = Depends(like_permission)
) -> ReactionRead:
    created_post = await reaction_service.set(
        user_id=user.id,
        post_id=post_id,
        new_reaction=new_reaction
    )
    return created_post


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reaction(post_id: int, user: UserRead = Depends(like_permission)):
    await reaction_service.delete(post_id=post_id, user_id=user.id)
