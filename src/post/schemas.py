from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    text: str
    published: bool


class PostRead(PostBase):
    id: int
    author_id: int
    text: str
    published: bool
    create_data: datetime
    update_date: datetime
    likes: int = 0
    dislikes: int = 0


class PostUpdate(PostBase):
    text: Optional[str] = None
    published: Optional[bool] = None
