from typing import Optional

from fastapi import HTTPException as StarletHTTPException
from fastapi import status


class ReactionPermissionException(StarletHTTPException):
    def __init__(self, headers: Optional[dict[str, str]] = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to like your posts.",
            headers=headers,
        )
