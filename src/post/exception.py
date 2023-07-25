from typing import Optional

from fastapi import HTTPException as StarletHTTPException


class AuthorPermissionException(StarletHTTPException):
    def __init__(self, headers: Optional[dict[str, str]] = None) -> None:
        super().__init__(
            status_code=403,
            detail="Action available to the author only",
            headers=headers,
        )
