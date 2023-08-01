from fastapi import Depends, Request

from src.auth.config import current_user
from src.auth.schemas import UserRead
from src.post.reaction.exception import OwnPostReactionPermissionException
from src.post.services import post_service


async def like_permission(request: Request, user: UserRead = Depends(current_user)):
    post_id = int(request.path_params["post_id"])
    post = await post_service.get(post_id)
    if user.id == post.author_id:
        raise OwnPostReactionPermissionException
    return user
