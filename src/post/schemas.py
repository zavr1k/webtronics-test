from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .types import ReactionType


class MyBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PostCreate(MyBaseModel):
    text: str
    published: bool


class PostRead(MyBaseModel):
    id: int
    author_id: int
    text: str
    published: bool
    create_data: datetime
    update_date: datetime
    likes: int = 0
    dislikes: int = 0


class PostUpdate(MyBaseModel):
    text: Optional[str] = None
    published: Optional[bool] = None


class ReactionCreate(MyBaseModel):
    reaction: ReactionType


class ReactionRead(MyBaseModel):
    id: int
    user_id: int
    post_id: int
    reaction: ReactionType
    create_data: datetime
    update_date: datetime
